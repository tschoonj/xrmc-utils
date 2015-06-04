;prepare inputfile for dscan
SPAWN, '../../bin/xrmc-dscan input.dat y -0.1 0.1 20', EXIT_STATUS=status
IF (status NE 0) THEN MESSAGE, 'Failure executing xrmc-dscan'

;execute inputfile with xrmc
;SPAWN, 'xrmc dscan-input.dat'
;IF (status NE 0) THEN MESSAGE, 'Failure executing xrmc'

;read in the outputfiles
data = []
FOR i=0,20 DO BEGIN
	filename = STRING('output_', i, '.dat', FORMAT='(A,I0,A)')
	raw_data = xrmc_read_angio_image2(filename)
	; extract Fe-Ka
	data = [data, TOTAL(raw_data.data[*,307:334,0,0])]
ENDFOR

my_plot = plot(data)

END
