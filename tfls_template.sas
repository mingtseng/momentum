/*************************************************************************************************
File name:

Study: 

SAS version:    9.4

Purpose:

Macros called:  

Notes:          

Parameters:     

Sample:         

Date started:
Date completed: 

**Per QA request, please update the modification history follow the format in the 1st line.**

Mod     Date            Name            Description
---     -----------     ------------    -----------------------------------------------
1.0

************************************ Prepared by CLT Inc. ************************************/
** ------------------------------------------------ *;
** initialize study path
** ------------------------------------------------ *;
Data _null_;
	call execute('%global _programname; %let _fullpath = %sysfunc(GetOption(SYSIN));'); 
	call execute('%nrstr(data _null_; if lengthn("%sysfunc(GetOption(SYSIN))")=0 then call execute('||
	     '"%nrstr(%let _fullpath = %sysget(SAS_EXECFILEPATH);)");run;)');
	call execute('%nrstr(%let _programname=%sysfunc(kscan(%sysfunc(kscan(&_fullpath,-1,\)),1,.));)');
Run;

%inc "%substr(&_fullpath.,1,%eval(%length(&_fullpath.)-%index(%sysfunc(reverse(&_fullpath.)),\)))\0-init.sas";

** ------------------------------------------------ *;
** Set study common info 
** ------------------------------------------------ *;
%inc "&_programpath.\commonproc.sas";

** ------------------------------------------------ *;
** generate info for tfl title,footnote and so on
** ------------------------------------------------ *;
%top_info(TopDs=TOP2,debug=0);

** ------------------------------------------------ *;
** 					Minecraft
** ------------------------------------------------ *; 


** ------------------------------------------------ *;
** Set ods style and ods destination for tfls
** ------------------------------------------------ *; 
%RTFtemp()

** ------------------------------------------------ *;
** close ods destination 
** ------------------------------------------------ *;
%ods_close();
