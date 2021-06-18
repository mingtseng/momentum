/*****************************************************
offsetmax: 图形plot与绘图区顶部的偏移距离
offsetmin: 图形plot与绘图区底部的偏移距离
griddisplay: 显示刻度线
display: 轴线, 刻度标记, 刻度值, 标签
markercharacter: 给每个坐标添加标记字符,选项值可以是变量名
labelstrip: 给标签或标记值去除空格
labelposition: 标签位置

******************************************************/
proc template;
	define statgraph Fig_6_2_1;
		begingraph / subpixel=on;
			entrytitle "Mileage by Type";
			layout overlay / xaxisopts=(display=(ticks tickvalues))
							 yaxisopts=(label="Mean Mileage" griddisplay=on offsetmin=0.25 labelposition=datacenter)
							 y2axisopts=(offsetmin=0.05 offsetmax=0.8 display=(ticks tickvalues));
				barchart x=type y=mpg_city / stat=mean dataskin=crisp;
				scatterplot x=typemean y=NLabel / markercharacter=n labelstrip=true yaxis=y2;
				scatterplot x=typemean y=MeanLabel / markercharacter=mean labelstrip=true yaxis=y2;
				scatterplot x=typemean y=MedianLabel / markercharacter=median labelstrip=true yaxis=y2;
			endlayout;
		endgraph;
	end;
run;
ods listing close;
ods html;
proc sgrender template=Fig_6_2_1 data=GTL_GS_Cars;
run;
ods html close;


/*****************************************************
tickvaluelist: 需要显示的刻度值列表
tickvaluesequence: 刻度值范围及其间隔(start=0 end=50 increment=10)
tickvaluepriority: 让所有数据都在刻度值范围内显示
******************************************************/
proc template;
	define statgraph Fig_6_2_2;
		begingraph;
			entrytitle "Mileage by Horsepower";
			layout overlay / xaxisopts=(griddisplay=on linearopts=(tickvaluelist=(150 200 250 300 350)))
							 yaxisopts=(griddisplay=on linearopts=(tickvaluepriority=true tickvaluesequence=(start=0 end=50 increment=10)));
				scatterplot x=horsepower y=mpg_city;
			endlayout;
		endgraph;
	end;
run;

ods html;
proc sgrender template=Fig_6_2_2 data=GTL_GS_Cars;
run;
ods html close;

/*****************************************************
tickdisplaylist: 刻度值标签
******************************************************/
proc template;
	define statgraph Fig_6_2_3;
		begingraph / subpixel=on;
			entrytitle "Mean Mileage by Make";
			layout overlay / xaxisopts=(display=(tickvalues) 
										discreteopts=(tickvaluefitpolicy=split 
													  tickvaluelist=('Acura' 'Audi' 'BMW' 'Lexus' 'Mercedes-Benz' 'Porsche')
													  tickdisplaylist=('Acura' 'Audi' 'BMW' 'Lexus' 'Mercedes Benz' 'Porsche')
										)
							  );
				barchart x=make y=mpg_city / stat=mean dataskin=crisp barlabel=true;
			endlayout;
		endgraph;
	end;
run;
ods html;
proc sgrender template=Fig_6_2_3
	data=sashelp.cars(where=(msrp > 60000));
run;
ods html close;


data cars;
	set sashelp.cars;
	if Make="Acura";
	keep horsepower msrp;
run;
proc template;
	define statgraph Fig_6_2_4;
		begingraph;
			entrytitle "MSRP by Horsepower";
			layout overlay / xaxisopts=(type=log griddisplay=on logopts=(base=2 tickintervalstyle=linear))
							 yaxisopts=(griddisplay=on linearopts=(tickvaluepriority=true tickvaluelist=(10000 50000 100000 200000)));
				scatterplot x=horsepower y=msrp;
			endlayout;
		endgraph;
	end;
run;
proc sgrender template=Fig_6_2_4 data=sashelp.cars;
run;

proc template;
	define statgraph Fig_8_2;
		begingraph;
			entrytitle "Mileage by Type";
			layout overlay / xaxisopts=(display=(ticks tickvalues))
							 yaxisopts=(griddisplay=on);
				barchart x=type y=mpg_city / stat=mean dataskin=gloss fillattrs=graphdata4(transparency=0.3);
			endlayout;
		endgraph;
	end;
run;
ods html;
proc sgrender template=Fig_8_2 data=sashelp.cars(where=(type ne "Hybrid"));
run;
ods html close;
		
