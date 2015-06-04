;prepare inputfile for dscan
SPAWN, '../../bin/xrmc-dmesh input.dat x -0.1 0.1 10 y -0.1 0.1 10', EXIT_STATUS=status
IF (status NE 0) THEN MESSAGE, 'Failure executing xrmc-dmesh'

;execute inputfile with xrmc
SPAWN, 'xrmc dmesh-input.dat'
IF (status NE 0) THEN MESSAGE, 'Failure executing xrmc'

;read in the outputfiles
data = dblarr(21,21) 
FOR i=0,20 DO BEGIN
FOR j=0,20 DO BEGIN
	filename = STRING('output_', i, '_', j, '.dat', FORMAT='(A,I0,A,I0,A)')
	raw_data = xrmc_read_angio_image2(filename)
	; extract Fe-Ka
	data[i,j] = TOTAL(raw_data.data[*,307:334,0,0])
ENDFOR
ENDFOR

;my_plot = plot(data)

END
