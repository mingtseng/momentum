PROC TEMPLATE;
		/* define部分 */
    define statgraph GraphTemplateName;
        MVAR pageth numpage;
		/* begingraph */
        begingraph / designwidth = 10 designheight = 7.5 border = false;

 
            entrytitle halign = left "广州南新制药有限公司"  halign = right "Page " pageth " of " numpage /outerpad=(bottom=0.1px);
            entrytitle halign = left "头孢呋辛酯分散片-餐后试验" halign = right "统计分析报告" / outerpad=(bottom=0.1px);
            entrytitle " ";
			entrytitle "图 8-1-1: 平均血药浓度-时间曲线（算术坐标）- PK浓度集" / pad=(right=5px) outerpad=(bottom=0.1px) haligncenter = graph;

			entryfootnote halign = left "注：血样采集时间点依次为" / pad=(right=5px) outerpad=(bottom=0.1px);
            entryfootnote halign = left "Input Dataset: ADAM.ADPC" / pad=(right=5px) textattrs=(size=8pt);
            entryfootnote halign = left "SOURCE: ..\tbfxz\stat\testdir\program\tfl\ftbfxzcs1-8-1-1.sas zengming SAS9.4 (Rawdata Version: 19JAN2021, Output Date: 21JAN2021 15:50)" / pad=(right=5px) textattrs=(size=8pt);


/*            &legenditemText.*/
/*            discreteattrmap name="AttrMap" / ignorecase=true ;*/
/*            &AtttrMapText.*/
/*            enddiscreteattrmap ;*/
/*            discreteattrvar attrvar=_Group_AttrMap var=_Group attrmap="AttrMap" ;*/
/*            discreteattrvar attrvar=_Group_AttrMap1 var=_Group1 attrmap="AttrMap" ;*/
/*            discreteattrvar attrvar=_Group_AttrMap2 var=_Group2 attrmap="AttrMap" ;*/

        %if %length(&LayoutStatements.)=0 %then %do;
        layout lattice / rowweights=&rowweights. columndatarange=union rowdatarange=union columns=1;
            sidebar / align = left; layout gridded / border = false WIDTH = &LeftsideSpace.; entry " " ; endlayout; endsidebar;
            sidebar / align = right; layout gridded / border = false WIDTH = &RightsideSpace.; entry " " ; endlayout; endsidebar;

            %* Plot cell ;
            layout overlay / PAD = (bottom = 2px)
                xaxisopts = (offsetmin = 0.01 offsetmax = 0.01 display=(ticks tickvalues) linearopts = (TICKVALUEFITPOLICY = none tickvaluelist=(&XTickValueList.)) &XaxisOpts.)
                yaxisopts = (offsetmin = 0.01 offsetmax = 0.01 display=(ticks tickvalues) linearopts=(tickvaluepriority=true THRESHOLDMIN=1 THRESHOLDMAX=1) &YaxisOpts.)
                y2axisopts = (offsetmin = 0.01 offsetmax = 0.01 display=(ticks tickvalues) linearopts=(tickvaluepriority=true THRESHOLDMIN=1 THRESHOLDMAX=1) &Y2axisOpts.);

                %* draw on x-axis ;
                layout gridded / location=outside;
                        entry "采集时间点(h)" / pad=(bottom=5px top=5px) textattrs=(size=12);
                endlayout;

                %* draw on y-axis;
                layout gridded / location=outside halign=left order=columnmajor;
                        entry "血药浓度(ng/ml)平均值(+/-)标准误" / pad=(bottom=5px top=5px) rotate=90 textattrs=(size=12);
                endlayout;

                ScatterPlot X = Xvar Y = Yvar1 / JITTER= none
                    yaxis=y Group = _Group_AttrMap1 YErrorUpper = _upper1 YErrorLower = _lower1 includemissinggroup=false name = "Legend1";;

                SeriesPlot  X = Xvar Y = Yvar1 /
                    yaxis=y Group = _Group_AttrMap1 display = (markers) includemissinggroup=false name = "Legend1";;
                &PlotStatements.;

                %* draw on y2-axis;
                layout gridded / location=outside halign=right order=columnmajor; 
                        entry "%scan(%nrbquote(&y2label.),&i,$)  " / pad=(bottom=5px top=5px)  rotate=90 textattrs=(size=&FontSize_Label.);
                endlayout;

                ScatterPlot X = Xvar Y = Yvar2 / JITTER= none
                    yaxis=y2 Group = _Group_AttrMap2 YErrorUpper = _upper2 YErrorLower = _lower2 includemissinggroup=false name = "Legend2";;

				SeriesPlot  X = Xvar Y = Yvar2 /
                    yaxis=y2 Group = _Group_AttrMap2 display = (markers) includemissinggroup=false name = "Legend2";;
                &PlotStatements.

                DiscreteLegend
                        %if %length(&legenditemlist.)>0 %then %do; 
                            &legenditemlist.
                        %end;
                        %else %do; 
                            "Legend1" %if "&Y2axisfl."="1" %then "Legend2";
                        %end;
                    / Location = Outside Across = 5  Border = false DISPLAYCLIPPED = true ITEMSIZE=(LINELENGTH=20px)
                    &LegendOpts.;

                %* finally display the referenceline;
                    Referenceline y=0 / curvelabel="Reference Line";

                %* additional entry;
                    entry "additional entry";
            endlayout;

            %* block ;
                layout overlay / WALLDISPLAY = none yaxisopts = (display = none)
                        xaxisopts = (display = none offsetmin = 0.01 offsetmax = 0.01 linearopts = (TICKVALUEFITPOLICY = none tickvaluelist=(&XTickValueList.))
                            &XaxisOpts.);
                    innermargin / align = top ;
                        axistable x = _Xvar value = _n / CLASS = _Group_AttrMap COLORGROUP = _Group_AttrMap
						HEADERLABEL="%nrbquote(&BlockHeader.)" 
						HEADERLABELATTRS=(size=&FontSize_Block.) valueattrs=(size=&FontSize_Block.) labelattrs=(size=&FontSize_Block.);
                    endinnermargin;
                endlayout;
            %end;

        endlayout;%*End of layout lattice;
        %end;
    endgraph;
    end;
RUN;
