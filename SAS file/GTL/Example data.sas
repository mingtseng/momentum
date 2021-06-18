/*--4_2_2 Data Set SeriesGroupState--*/ 
data GTL_GS_SeriesGroup; 
format Date Date9.; 
do i=0 to 334 by 30; 
	date='01jan2009'd+i; 
	if mod (i, 30) =0 then freq=1; else freq=0; 
	Drug='Drug A'; Val = 16+ 3*sin(i/90+0.5) + 1*sin(3*i/90+0.7); output; 
	Drug='Drug B'; Val = 10+ 3*sin(i/90+0.5) + 1*cos(3*i/90+0.7); output; 
	Drug='Drug C'; Val =  6+ 3*cos(i/90+0.5) + 1*sin(3*i/90+0.7); output; 
end; 
run;

/*--4_2_3 Data Set SeriesGroupState--*/ 
data GTL_GS_stepGroup; 
format Date Date9.; 
do i=0 to 334 by 40; 
	date='01jan2009'd+i; 
	if mod (i, 30) =0 then freq=1; else freq=0; 

	Drug='Drug A'; Val = 16+ 3*sin(i/90+0.5) + 1*sin(3*i/90+0.7); 
	upper=val*1.1; lower=val*0.95; output; 

	Drug='Drug B'; Val = 11+ 3*sin(i/90+0.5) + 1*cos(3*i/90+0.7); 
	upper=val*1.1; lower=val*0.95; output;

	if i > 150 and i < 210 then val=.;
	else Val = 7+ 3*cos(i/90+0.5) + 1*sin(3*i/90+0.7);
	 
	Drug='Drug C'; upper=val*1.1; lower=val*0.95; output; 
end; 
run;
/*proc print;run; */

/*--4_2_4 Band Group--*/ 
data GTL_GS_bandGroup; 
format Date Date9.; 
do i=0 to 334 by 1; 
date='01jan2009'd+i; 
if mod (i, 30) =0 then freq=1; else freq=0; 
Drug='Drug A'; Val = 16+ 3*sin(i/90+0.5) + 1*sin(3*i/90+0.7); upper=val*1.1; lower=val*0.95; output; 
Drug='Drug B'; Val = 11+ 3*sin(i/90+0.5) + 1*cos(3*i/90+0.7); upper=val*1.1; lower=val*0.95; output; 
Drug='Drug C'; Val = 12+ 3*cos(i/90+0.5) + 1*sin(3*i/90+0.7); upper=val*1.1; lower=val*0.95; output; 
end; 
run; 

/*--4_2_6 HIGHLOW--*/ 
data GTL_GS_highlow; 
length cap $ 12; 
input drug $ low high cap $; 
datalines; 
A      10 20 NONE 
A      30 60 NONE 
B      20 35 NONE 
B      50 75 NONE 
C      30 90 FILLEDARROW 
; 
run;

/*--4_2_8 Needle--*/ 
data GTL_GS_NeedleLabel; 
format Date Date9.;
format a 4.3; 
do i=0 to 334 by 30; 
date='01jan2009'd+i; A = 16+ 3*sin(i/90+0.5) + 1*sin(3*i/90+0.7); output; 
end; 
run;

/*--4_2_9 Data Set VECTOR--*/ 
data GTL_GS_vector;
format label 3.0; 
do i=1 to 10; 
x=ranuni(2); xo=x*(1+(ranuni(2)-0.5)); 
y=ranuni(2); yo=y*(1+(ranuni(2)-0.5)); 
if (ranuni(2) < 0.5) then Type='A'; 
else Type='B';
label=(2*x+3*y); 
output; 
end; 
run; 

/*--Fig 4.3.4 Sedans vs rest--*/
proc sort data=sashelp.cars out=CarsCyOrigin;
  by origin;
  run;

data GTL_GS_Sedans;
  retain Sedans 0 Rest 0;
  format Pct percent.; 
  keep Origin Type Count Pct;
  set CarsCyOrigin;
  by origin;

  if first.origin then do; Sedans=0; Rest=0; end;

  if type eq 'Sedan' then Sedans+1;
  else  Rest+1;
  if last.origin then do;
    Type='Sedans'; Count=Sedans; Pct=count/(sedans+rest); output;
	Type='Rest';   Count=Rest;   Pct=count/(sedans+rest); output;
  end;
  run;
/*  proc print;run;*/

/*--Fig 4.3.4 Sedans vs rest--*/
data GTL_GS_IntervalBoxGroup;
  format Date date6.;
  drop i;
  do Date='01Jan2009'd, '15Jan2009'd,'15Mar2009'd,
          '01May2009'd, '01Aug2009'd; 
    do i=1 to 10;
	  Response=rannorm(2); Drug='A'; output;
	  Response=ranuni(2);  Drug='A'; output;
	  Response=rannorm(2); Drug='B'; output;
	  Response=ranuni(2);  Drug='B'; output;
	end;
  end;
run;

/*--Fig 4.6.2 Heat map--*/
data GTL_GS_HeatmapParm;
  drop pi val;
  pi=constant('Pi');
  do x=1 to 20;
    do y=1 to 10;
	  value=sin(x*pi/10) + cos(y*pi/10);
	  val=ranuni(2);
      group=ifc(val < 0.5, 'M', 'F');
	  output;
	end;
  end;
run;
proc print data=GTL_GS_HeatmapParm; run;

/*--Fig 4.6.3--*/
data GTL_EllipseParm;
  input x y semimajor semiminor slope group $;
  datalines;
60  60  90 60  0 M 
50  40  70 40  1 F
;
run;

data GTL_EllipseParm_Class;
  set sashelp.class GTL_EllipseParm;
  if semimajor=. then semimajor=1;
  if semiminor=. then semiminor=1;
  if x=. then x=-50;
  if y=. then y=-50;
  run;

/*--Fig 4.6.5 Surface Plot--*/
data nums;
  do i=1 to 30;
     X=10*ranuni(33)-5;
     Y=10*ranuni(35)-5;
     Z=sin(sqrt(x*x+y*y));
     output;
  end;
run; 

proc g3grid data=nums out=GTL_GS_Gridded;
  grid y*x=z / spline 
               axis1=-5 to 5 by .1
               axis2=-5 to 5 by .1;
run;

proc sort data=GTL_GS_Gridded; 
by y x; 
run;

/*--Figure 4.6.6 Bivariate Histogram--*/
data heart;
  set sashelp.heart(keep=height weight);
    if height ne . and weight ne .; 
  height=round(height,5);
  weight=round(weight,25);
run;
 
 proc summary data=heart nway completetypes; 
  class height weight;
  var height;
  output out=GTL_GS_HeartStats(keep=height weight count) N=Count;
run;

/*--Fig 4.7.3 Survival plot from sashelp.BMT--*/
ods trace on;
ods output Survivalplot=GTL_GS_SurvivalPlotData;
ods graphics / reset imagename='Survival-LifeTest';
proc lifetest data=sashelp.BMT plots=survival(atrisk=0 to 2500 by 500);
   time T * Status(0);
   strata Group / test=logrank adjust=sidak;
   run;
ods trace off;

proc format;
  value aml
  3 = 'AML-Low'
  2 = 'AML-High'
  1 = 'All';
run;
 

/*ods html;*/
/*proc print data=odscg11.SurvivalPlotData;run;*/
/*ods html close;*/
/*proc print data=GTL_GS_SurvivalPlotData; run;*/

/*--Fig 5.2.6 Labs--*/
data GTL_GS_Labs;
  pi=constant('PI');
  do Lab='Lab-1', 'Lab-2', 'Lab-3';
    amp=100*ranuni(3);
	phase=pi*ranuni(2);
    do day=1 to 300 by 5;
	  Value=amp*(1+0.1*(sin(day*pi/180+phase)+0.2*ranuni(2)));
	  output;
	end;
  end;
run;
/*proc print;run;*/

/*--Fig 5.2.7 Labs2--*/
data GTL_GS_Labs2;
  pi=constant('PI');
  do Lab='Lab-1', 'Lab-2', 'Lab-3', 'Lab-4', 'Lab-5', 'Lab-6';
    amp=100*ranuni(4);
	phase=2*pi*ranuni(3);
    do day=1 to 300 by 5;
	  Value=amp*(1+0.1*(sin(day*pi/180+phase)+0.2*ranuni(5)));
	  output;
	end;
  end;
run;

/*--Fig_5_5_1 Lab Values by Study Week--*/
data GTL_GS_Labs_by_Week;
label sgot="SGOT";
label aph="ALKPHOS";
label visit="Study Week";
input visit $ 1-10 treatment $ sgot aph;
datalines;
SCREENING   PLACEBO       .        108.943
WEEK 2      PLACEBO     10.2941     83.740
WEEK 4      PLACEBO     16.1765     76.423
WEEK 6      PLACEBO     17.6471     86.179
WEEK 8      PLACEBO     11.7647     67.480
WEEK 10     PLACEBO     14.7059     68.293
WEEK 12     PLACEBO     13.2353     73.171
WEEK 14     PLACEBO     12.5000     74.797
SCREENING   ACTIVE      12.5000     66.667
WEEK 2      ACTIVE      17.3077     57.961
WEEK 4      ACTIVE      17.9487     68.873
WEEK 6      ACTIVE      26.9231     98.748
WEEK 8      ACTIVE      25.9615     98.211
WEEK 10     ACTIVE      27.2436    100.179
WEEK 12     ACTIVE      29.9679    104.293
WEEK 14     ACTIVE      26.9231    115.921
;
run;



/*--Fig_5_5_2 LFT Lattice--*/
data GTL_GS_LFT_Lattice (keep=drug alat biltot alkph asat
     palat pbiltot palkph pasat visitnum);
  label alat="ALAT (/ULN)";
  label biltot="BILTOT (/ULN)";
  label alkph="ALKPH (/ULN)";
  label asat="ASAT (/ULN)";
  visitnum=1;
  do i= 1 to 100;
    palat = min (4, 2.5 * (abs(rannor(123))) / 3.0);
    pbiltot = min (4, 2.5 * (abs(rannor(123))) / 3.0);
    palkph = min (4, 2.5 * (abs(rannor(123))) / 3.0);
    pasat = min (4, 2.5 * (abs(rannor(123))) / 3.0);
    alat = min (4, 2.5 * (abs(rannor(345))) / 3.0);
    biltot = min (4, 2.5 * (abs(rannor(345))) / 3.0);
    alkph = min (4, 2.5 * (abs(rannor(345))) / 3.0);
    asat = min (4, 2.5 * (abs(rannor(345))) / 3.0);
      j =  rannor(345);
      if j > 0 then drug = "A";
      else drug="B";
      output;
   end;
  visitnum=2;
  do i= 1 to 100;
    palat = min (4, 2.5 * (abs(rannor(789))) / 3.0);
    pbiltot = min (4, 2.5 * (abs(rannor(789))) / 3.0);
    palkph = min (4, 2.5 * (abs(rannor(789))) / 3.0);
    pasat = min (4, 2.5 * (abs(rannor(789))) / 3.0);
    alat = min (4, 2.5 * (abs(rannor(567))) / 3.5);
    biltot = min (4, 2.5 * (abs(rannor(567))) / 3.5);
    alkph = min (4, 2.5 * (abs(rannor(567))) / 3.5);
    asat = min (4, 2.5 * (abs(rannor(567))) / 3.5);
      j =  rannor(567);
      if j > 0 then drug = "A";
      else drug="B";
      output;
   end;
  visitnum=3;
  do i= 1 to 100;
    palat = min (4, 2.5 * (abs(rannor(321))) / 3.0);
    pbiltot = min (4, 2.5 * (abs(rannor(321))) / 3.0);
    palkph = min (4, 2.5 * (abs(rannor(321))) / 3.0);
    pasat = min (4, 2.5 * (abs(rannor(321))) / 3.0);
    alat = min (4, 2.5 * (abs(rannor(975))) / 2.5);
    biltot = min (4, 2.5 * (abs(rannor(975))) / 2.5);
    alkph = min (4, 2.5 * (abs(rannor(975))) / 2.5);
    asat = min (4, 2.5 * (abs(rannor(975))) / 2.5);
      j =  rannor(975);
      if j > 0 then drug = "A";
      else drug="B";
      output;
   end;
run;

proc format;
value wk
  1='1 Week'
  2='3 Months'
  3='6 Months';
value lab
  1='ALAT'
  2='Bilirubin Total'
  3='Alk Phosphatase'
  4='ASAT';
value $trt
  "A"="Drug A (n=240)"
  "B"="Drug B (n=195)";
run;

data GTL_GS_LFT_Lattice2 (keep=visitnum drug labtest result pre);
format visitnum wk. labtest lab. drug $trt.;
label pre='Baseline (/ULN) *' result='Study (/ULN)';
set GTL_GS_LFT_Lattice;
  pre=palat;
  labtest=1;
  result=alat;
  output;
  pre=pbiltot;
  labtest=2;
  result=biltot;
  output;
  pre=palkph;
  labtest=3;
  result=alkph;
  output;
  pre=pasat;
  labtest=4;
  result=asat;
  output;
run;
	  

/*--Fig_5_5_3 Most Frequend AE--*/
data GTL_GS_AE;
  input ae $1-30 a b low mean high;
  label a='Percent';
  label b='Percent';
  datalines;
ARTHRALGIA                    1   3    1    7     48
NAUSIA                        4   18   2    4     8  
ANOREXIA                      2   3    0.9  3.8   16
HEMATURIA                     2   4    0.8  3.2   15
INSOMNIA                      3   5.5  1.1  3.0   7
VOMITING                      3.5 6    1.2  2.5   6
DYSPEPSIA                     4   10   1.1  2.4   4.5
HEADACHE                      7   10   0.8  1.1   2
BACK PAIN                     5   6    0.8  1.04  2
COUGHING                      8   8    0.5  1.0   2
MYALGEA                       4   4    0.4  1.0   1.9
MELENA                        4.5 4    0.4  0.9   2.2
RHINITIS                      7   6    0.4  0.9   1.9
BRONCHITIS                    5   3.5  0.3  0.7   2
CHEST PAIN                    6   4    0.3  0.8   1.8
DYSPNEA                       7   2.5  0.13 0.3   0.7
;
run;

proc sort data=GTL_GS_AE out=GTL_GS_AE;
  by mean;
  run;

data GTL_GS_AE_Ref;
  set GTL_GS_AE;
  if mod(_n_, 2) ne 0 then refae=ae;
  run;

/*--Fig_6_2_1 Common Axis Opts--*/
proc means data=sashelp.cars noprint;
  class type;
  var mpg_city;
  output out=CarsMeanMileage
         n=N
         mean=Mean
         median=Median;
run;

data GTL_GS_Cars;
  format mean median 4.1;
  set sashelp.cars CarsMeanMileage(where=(_type_ eq 1) 
                                   rename=(type=TypeMean));
  if(typemean ne 'Hybrid');
  if(type ne 'Hybrid');
  NLabel='N'; meanLabel='Mean'; medianLabel='Median';
  run;
proc print data=GTL_GS_Cars;run;

/*--Fig_7_2_1 Group Series Discrete Attr Map--*/
data GTL_GS_Series_Dis_Attr_Map;
format Date Date9.; 
do i=0 to 334 by 30; 
date='01jan2009'd+i; 
if mod (i, 30) =0 then freq=1; else freq=0; 
Drug='Drug A'; Val = 16+ 3*sin(i/90+0.5) + 1*sin(3*i/90+0.7); output; 
Drug='Drug C'; Val =  6+ 3*cos(i/90+0.5) + 1*sin(3*i/90+0.7); output; 
end; 
run;

/*--7_2_2 HIGHLOW Discrete Attr Map--*/ 
data GTL_GS_highlow_Dis_Attr_Map; 
length cap $ 12; 
input drug $ low high cap $; 
datalines; 
A      10 20 NONE 
A      30 60 NONE 
B      20 35 NONE 
B      50 75 NONE 
C      30 90 FILLEDARROW 
; 
run;

