data mydata;
	length automaker $30;
	input automaker $ 1-30 million_units;
	format million_units 3.1;
	select (automaker);
		when ("Fiat") do;
			colorvar=1;
			call symput("fwidth",million_units);
		end;
		when ("Chrysler") do;
			colorvar=1;
			call symput( "cwidth", million_units);
		end;
		when ("Fiat + Chrysler") do;
			colorvar=2;
			call symput( "cfwidth", million_units);
		end;
		otherwise colorvar=3;
		end;
	datalines;
Toyota						    8.7
GM 								7.7
Volkswagen 						6.0
Renault-Nissan 				    5.8
Ford 							5.4
Fiat + Chrysler				    4.5
Hyundai		   				    4.2
Honda 							3.8
PSA 							3.2
Fiat 							2.5
Suzuki 							2.4
Chrysler 						2.0
Daimler 						1.9
BMW 							1.4
Mazda							1.4
Mitsubishi						1.1
;
run;
ods html;
proc template;
	define statgraph automerger;
		begingraph / drawspace=datavalue;
			entrytitle halign=center 'Top Global Automakers (2008 Annual Unit Sales)';
			layout lattice / rowdatarange=data columndatarange=data rowgutter=10 columngutter=10;
				layout overlay / xaxisopts=(label=('Units (millions)'))
								 yaxisopts=(reverse=true display=(ticks tickvalues line));

					barchart category=automaker response=million_units / group=colorvar
							 name='bar(h)' barlabel=true dataskin=pressed orient=horizontal;
					drawrectangle x=eval(&cwidth/2.0) y="Chrysler"
								  width=&cwidth height=0.95 / widthunit=data heightunit=data
								  display=(outline) outlineattrs=(color=yellow);
					drawrectangle x=eval(&fwidth/2.0) y="Fiat"
								  width=&fwidth height=0.95 /
								  widthunit=data heightunit=data
								  display=(outline) outlineattrs=(color=yellow);
					drawrectangle x=eval(&cfwidth/2.0) y="Fiat + Chrysler"
								  width=&cfwidth height=0.95 / widthunit=data heightunit=data
								  display=(outline) outlineattrs=(color=yellow);
					beginpolyline x=eval(&cwidth + 0.5) y="Chrysler";
						draw x=eval(&cwidth + 1.5) y="Chrysler";
						draw x=eval(&cwidth + 1.5) y="Fiat";
						draw x=eval(&fwidth + 0.5) y="Fiat";
					endpolyline;
					beginpolyline x=eval(&cwidth + 1.5) y="Suzuki";
						draw x=eval(&cfwidth + 1.5) y="Suzuki";
						draw x=eval(&cfwidth + 1.5) y="Fiat + Chrysler";
					endpolyline;
					drawarrow x1=eval(&cfwidth + 1.5) x2=eval(&cfwidth + 0.5)
							  y1="Fiat + Chrysler" y2="Fiat + Chrysler"
							  / arrowheadscale=0.5 arrowheadshape=barbed;
					drawtext "Alliance creates the #6 Global Automaker by volume" /
							 y="Honda" x=eval(&cfwidth+2.5) width=2 widthunit=data;
				endlayout;
			endlayout;
		endgraph;
	end;
run;
proc sgrender data=mydata template=automerger;
run;
