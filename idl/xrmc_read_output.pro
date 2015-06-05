FUNCTION xrmc_read_output, filename, ModeNum, Nx, Ny, NBins

OPENR, lun, filename, /get_lun

IF (N_PARAMS() EQ 1) THEN BEGIN
	ModeNum = 0L
	NX = 0L
	NY = 0L
	PixelSizeX = 0.0D
	PixelSizeY = 0.0D
	ExpTime = 0.0D
	PixelType = 0L
	NBins = 0L
	Emin = 0.0D
	Emax = 0.0D

	readu, lun, ModeNum
	readu, lun, NX
	readu, lun, NY
	readu, lun, PixelSizeX
	readu, lun, PixelSizeY
	readu, lun, ExpTime
	readu, lun, PixelType
	readu, lun, NBins
	readu, lun, Emin
	readu, lun, Emax

ENDIF ELSE BEGIN
	PixelSizeX = 0.0D
	PixelSizeY = 0.0D
	ExpTime = 0.0D
	PixelType = 0L
	Emin = 0.0D
	Emax = 0.0D
ENDELSE

; I think it should be something like
;
data = DBLARR([NX, NY, NBins, ModeNum], /NOZERO)


;data = dblarr([NBins, Ny, Nx, ModeNum],/nozero)
READU,lun,data
FREE_LUN, lun
data = TEMPORARY(TRANSPOSE(data))

data = REFORM(data,[ModeNum, NBins, NY, NX],/overwrite)
struct = {$
	ModeNum:Modenum,$
	NX:NX,$
	NY:NY,$
	PixelSizeX:PixelSizeX,$
	PixelSizeY:PixelSizeY,$
	ExpTime:ExpTime,$
	PixelType:PixelType,$
	NBins:Nbins,$
	Emin:Emin,$
	Emax:Emax,$
	data:data $
}
	

RETURN, struct


END
