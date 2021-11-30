// Name: Ian Rolph
// ONID: 933-653-468
// Date: 11/1/2021
// Description: A program that mimics the functionality of a shell, including program execution
//				and signal handling.

#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>

// this is a terrible way of doing this but the alternative is much worse
int fgOnly = 0;

struct command {
	int numArgs;
	char* args[512]; // maximum of 512 args
	int runAsBG;
	char* redirectTo;
	char* redirectFrom;
};

void sigtstpHandler(int signo) {
	switch (fgOnly) {
	case 1:
		fgOnly = 0;
		const char* disableMessage = "\nExiting foreground - only mode\n\0";
		write(1, disableMessage, strlen(disableMessage));
		break;
	case 0:
		fgOnly = 1;
		const char* enableMessage = "\nEntering foreground-only mode (& is now being ignored)\n\0";
		write(1, enableMessage, strlen(enableMessage));
		break;
	}
	return;
}

void removeProcess(int* idArray, int id) {
	int i = 0;
	while (idArray[i] != 0) {
		if (idArray[i] == id) {
			idArray[i] = 0;
			int start = i + 1;
			while (idArray[start] != 0) {
				idArray[start - 1] = idArray[start];
				start++;
			}
			idArray[start - 1] = 0;
			break;
		}
		i++;
	}
}

void cleanupBgProcesses(int* processes) {
	int i = 0;
	while (processes[i] > 0) {
		kill(processes[i], SIGKILL);
		i++;
	}
}

void expandVariable(char* inputStr) {
	char* pos = strstr(inputStr, "$$");
	if (pos != NULL) {
		char newBuffer[2049];
		memset(newBuffer, 0, sizeof(newBuffer)); // clear buffer in case there's some stray bytes
		char pidStr[9]; // setting to 8 digits + null because i'm paranoid about process id lengths
		strncpy(newBuffer, inputStr, pos - inputStr);
		sprintf(pidStr, "%d", getpid());
		strcat(newBuffer, pidStr);
		strcat(newBuffer, pos + 2);
		strcpy(inputStr, newBuffer);
		expandVariable(inputStr);
	}
}

// make a command structure for easy(er) parsing
struct command* initCommandStruct(char* inputStr) {
	expandVariable(inputStr);
	struct command* newStruct = malloc(sizeof(struct command));
	newStruct->numArgs = 0;
	newStruct->runAsBG = 0;
	newStruct->redirectTo = NULL;
	newStruct->redirectFrom = NULL;
	char* savePtr;
	char* currToken;
	currToken = strtok_r(inputStr, "\n ", &savePtr);
	newStruct->args[newStruct->numArgs] = currToken; 
	newStruct->numArgs++;
	while ((currToken = strtok_r(NULL, "\n ", &savePtr)) != NULL) {
		newStruct->args[newStruct->numArgs] = currToken;
		newStruct->numArgs++;
	}
	newStruct->args[newStruct->numArgs] = NULL;
	if (strcmp(newStruct->args[newStruct->numArgs - 1], "&") == 0) {
		if (fgOnly == 0) {
			newStruct->runAsBG = 1;
		}
		newStruct->args[newStruct->numArgs - 1] = NULL;
	}
	int i = 0;
	for (i = 0; i < newStruct->numArgs; i++) {
		if (newStruct->args[i] != NULL && strcmp(newStruct->args[i], ">") == 0 && newStruct->args[i + 1] != NULL) {
			newStruct->redirectTo = newStruct->args[i + 1];
			newStruct->args[i] = NULL;
			newStruct->args[i+1] = NULL;
		}
		else if (newStruct->args[i] != NULL && strcmp(newStruct->args[i], "<") == 0 && newStruct->args[i + 1] != NULL) {
			newStruct->redirectFrom = newStruct->args[i + 1];
			newStruct->args[i] = NULL;
			newStruct->args[i + 1] = NULL;
		}
	}
	return newStruct;
}

int main() {
	int exitFlag = 0;
	int bgExitMethod = 0;
	int bgProcesses[512];
	memset(bgProcesses, 512, 0);
	int numBgProcesses = 0;
	char inputBuffer[2049]; // 2048 command line size + null char
	int lastExitStatus = 0;
	int lastSignalled = 0;
	pid_t bgpid;

	// set up necessary signal handlers for the shell
	struct sigaction sigIntAction = { {0} };
	sigIntAction.sa_handler = SIG_IGN; // shell should ignore sigint
	sigfillset(&sigIntAction.sa_mask);
	sigIntAction.sa_flags = SA_RESTART; // set flag for this one even though it doesn't really matter (just in case)
	sigaction(SIGINT, &sigIntAction, NULL);

	struct sigaction sigTstpAction = { {0} };
	sigTstpAction.sa_handler = sigtstpHandler; // toggle foreground-only mode
	sigfillset(&sigTstpAction.sa_mask);
	sigTstpAction.sa_flags = SA_RESTART; // flag must be set otherwise program segfaults when it returns
	sigaction(SIGTSTP, &sigTstpAction, NULL);

	// main shell prompt loop
	while (!exitFlag) {
		fflush(stdout);
		fflush(stdin);
		fflush(stderr);

		// before returning to the shell, check for any finished background processes
		bgpid = waitpid(-1, &bgExitMethod, WNOHANG);
		while (bgpid > 0) {
			if (WIFSIGNALED(bgExitMethod)) {
				printf("background pid %d is done: terminated by signal %d\n", bgpid, WTERMSIG(bgExitMethod));
			}
			else if (WIFEXITED(bgExitMethod)) {
				printf("background pid %d is done: exit value %d\n", bgpid, WEXITSTATUS(bgExitMethod));
			}
			removeProcess(bgProcesses, bgpid);
			numBgProcesses--;
			bgpid = waitpid(-1, &bgExitMethod, WNOHANG);
		}

		printf(": ");

		memset(inputBuffer, 0, 2049); // get rid of any stray bytes
		fgets(inputBuffer, 2048, stdin);

		// ignore blank lines and comments
		if (inputBuffer[0] == '\n' || inputBuffer[0] == '#') {
			continue;
		}
		else {
			struct command* cmdInput = initCommandStruct(inputBuffer);
			// handle built-in commands
			if (strcmp(cmdInput->args[0], "cd") == 0) {
				if (cmdInput->numArgs == 1) {
					chdir(getenv("HOME"));
				}
				else {
					int success = chdir(cmdInput->args[1]);
					if (success != 0) {
						printf("directory not found: %s\n", cmdInput->args[1]);
					}
				}
			}
			else if (strcmp(cmdInput->args[0], "status") == 0) {
				if (lastSignalled) {
					printf("terminated by signal %d\n", lastExitStatus);
				}
				else {
					printf("exit value %d\n", lastExitStatus);
				}
			}
			else if (strcmp(cmdInput->args[0], "exit") == 0) {
				exitFlag = 1;
			}
			// handle anything other than built-in commands
			else {
				int childExitMethod;
				pid_t spawnPid = fork();
				switch (spawnPid) {
				case -1: // fork failed for some reason
					printf("fork failed, time to log onto teach\n");
					break;
				case 0: // child process
					if (cmdInput->runAsBG == 0) {
						sigIntAction.sa_handler = SIG_DFL;
						sigaction(SIGINT, &sigIntAction, NULL); // make sure the process can be interrupted
					}
					sigTstpAction.sa_handler = SIG_IGN;
					sigaction(SIGTSTP, &sigTstpAction, NULL); // ignore ctrl+z in the child
					// handle output redirection
					if (cmdInput->redirectTo != NULL) {
						int out = open(cmdInput->redirectTo, O_WRONLY | O_CREAT | O_TRUNC, 0644);
						if (out == -1) {
							exit(1);
						}
						int result = dup2(out, STDOUT_FILENO);
						if (result == -1) {
							exit(2);
						}
					}
					else if (cmdInput->runAsBG == 1) {
						int out = open("/dev/null", O_WRONLY, 0644);
						if (out == -1) {
							exit(1);
						}
						int result = dup2(out, STDOUT_FILENO);
						if (result == -1) {
							exit(2);
						}
					}
					// handle input redirection
					if (cmdInput->redirectFrom != NULL) {
						int in = open(cmdInput->redirectFrom, O_RDONLY);
						if (in == -1) {
							printf("cannot open %s for input\n", cmdInput->redirectFrom);
							exit(1);
						}
						int result = dup2(in, STDIN_FILENO);
						if (result == -1) {
							exit(2);
						}
					}
					else if (cmdInput->runAsBG == 1) {
						int in = open("/dev/null", O_RDONLY);
						if (in == -1) {
							exit(1);
						}
						int result = dup2(in, STDIN_FILENO);
						if (result == -1) {
							exit(2);
						}
					}
					execvp(cmdInput->args[0], cmdInput->args);
					printf("%s: no such file or directory\n", cmdInput->args[0]);
					exit(EXIT_FAILURE);
					break;
				default: // parent process
					if (cmdInput->runAsBG == 0) {
						sigprocmask(SIG_BLOCK, &sigTstpAction.sa_mask, NULL); // block SIGTSTP signal as long as there's a foreground process
						spawnPid = waitpid(spawnPid, &childExitMethod, 0);
						if (WIFEXITED(childExitMethod)) {
							//printf("PARENT(%d): child(%d) terminated with exit method %d.\n", getpid(), spawnPid, WEXITSTATUS(childExitMethod));
							lastSignalled = 0;
							lastExitStatus = WEXITSTATUS(childExitMethod);
							
						}
						// if it didnt exit it was probably signaled
						else if (WIFSIGNALED(childExitMethod)) {
							//printf("PARENT(%d): child(%d) killed with signal %d.\n", getpid(), spawnPid, WTERMSIG(childExitMethod));
							printf("terminated by signal %d.\n", WTERMSIG(childExitMethod));
							lastSignalled = 1;
							lastExitStatus = WTERMSIG(childExitMethod);
						}
						sigprocmask(SIG_UNBLOCK, &sigTstpAction.sa_mask, NULL); // unblock SIGTSTP after foreground process ends
					}
					else {
						printf("background pid is %d\n", spawnPid);
						bgProcesses[numBgProcesses] = spawnPid;
						numBgProcesses++;
					}
					break;
				}
			}
			free(cmdInput);
		}
	}
	cleanupBgProcesses(bgProcesses); // kill all ongoing background processes upon exiting
}