;prepare inputfile for dmesh
;SPAWN, '../../bin/xrmc-dmesh input.dat y -0.1 0.1 20 x -0.1 0.1 20', EXIT_STATUS=status
;IF (status NE 0) THEN MESSAGE, 'Failure executing xrmc-dmesh'

;execute inputfile with xrmc
;SPAWN, 'xrmc dmesh-input.dat'
;IF (status NE 0) THEN MESSAGE, 'Failure executing xrmc'

;read in the outputfiles
data = dblarr(21,21) 
FOR i=0,20 DO BEGIN
FOR j=0,20 DO BEGIN
	filename = STRING('output_', i, '_', j, '.dat', FORMAT='(A,I0,A,I0,A)')
	raw_data = xrmc_read_output(filename)
	; extract Fe-Ka
	data[i,j] = TOTAL(raw_data.data[*,307:334,0,0])
ENDFOR
ENDFOR

loadct,3

tvlct,ct,/get

ct2=ct

ct2[*,0] = reverse(ct[*,0])
ct2[*,1] = reverse(ct[*,1])
ct2[*,2] = reverse(ct[*,2])


my_image = IMAGE(data, axis_style=2,rgb_table=ct2,title='Fe-Ka net-line intensities distribution',POSITION=[0.12,0.12,0.77,0.93],xtitle='# pixels',ytitle='# pixels')
my_cb = colorbar(target=my_image,orientation=1, textpos=1,tickdir=1,border_on=1,title='Counts (a.u.)',POSITION=[0.83,0.12,0.90,0.93])

openw, lun, 'ascii_output.dat', /get_lun
printf, lun, 2 
printf, lun, size(data, /dimensions)
printf, lun, data
free_lun, lun


END
