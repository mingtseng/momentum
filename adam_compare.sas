/*************************************************************************************************
File name: 

Study:          

sas version:    9.4

Purpose:        compare adam datasets
                

Macros called:  %qc_m_compare

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
Data _null_;
	call execute('%global _programname; %let _fullpath = %sysfunc(GetOption(SYSIN));'); 
	call execute('%nrstr(data _null_; if lengthn("%sysfunc(GetOption(SYSIN))")=0 then call execute('||
	     '"%nrstr(%let _fullpath = %sysget(SAS_EXECFILEPATH);)");run;)');
	call execute('%nrstr(%let _programname=%sysfunc(kscan(%sysfunc(kscan(&_fullpath,-1,\)),1,.));)');
Run;

%inc "%substr(&_fullpath.,1,%eval(%length(&_fullpath.)-%index(%sysfunc(reverse(&_fullpath.)),\)))\0-init.sas";

%macro ds_comp(ds=,lab=,dv=);

%let ds=%sysfunc(translate(&ds.,'_','-'));

proc datasets nolist nodetails nowarn lib=work; delete zhucheng fucheng/memtype=data; quit;
data zhucheng; 
    set tfl.&ds.;
run;
data fucheng;
    set tfl_qc.&ds.;
run;
%qc_m_compare(
  type     = tfl   
  ,base    = work.zhucheng
  ,compare = work.fucheng
  %if &dv =1 %then %do;
        ,dropvars =  _pageit_ maxlines _pageit_2
    %end;
    %if &dv =2 %then %do;
        ,dropvars =  _pageit_  
    %end;
    %if &dv =3 %then %do;
        ,dropvars =  _flnum _seq_ _pageit_ _pageit_2 maxlines 
    %end;
  %if &dv =5 %then %do;
        ,dropvars =  _flnum _seq_ 
    %end;
	%if &dv=6 %then %do;
        ,dropvars= page_seq maxlines
 %end;
  ,fresult =  &ds.   
  ,compvar = n );    
%mend;
