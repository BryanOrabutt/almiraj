#include <string.h>
#include <stdlib.h>
#include "soc_AM335x.h"
#include "beaglebone.h"

#include "consoleUtils.h"

int main()
{
	char* param = (char*)0x80030000;
	int x = 0;

	/* Initialize console for communication with the Host Machine */
    ConsoleUtilsInit();
    ConsoleUtilsSetType(CONSOLE_UART);
    ConsoleUtilsPrintf("Hello from Beaglebone Black\n\0");	

	//copy message
	strncpy(param, "Hello World\r\n\0", 14);

	while(1)
	{
		ConsoleUtilsPrintf(param);
		for(x = 0; x < 100000000; x++); //busy wait
	}

	return 0;
} 


