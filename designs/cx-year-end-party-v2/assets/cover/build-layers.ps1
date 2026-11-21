$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$coverRoot = $PSScriptRoot
$assetRoot = Split-Path $coverRoot -Parent
$refPath = Join-Path $assetRoot 'visual-reference.png'
$cleanPath = Join-Path $coverRoot '_generated-clean.png'
$haloSource = Join-Path $coverRoot '_generated-halo.png'
$mapSource = Join-Path $coverRoot '_generated-map.png'
$offsetY = 401
$canvasW = 1055
$canvasH = 2293

function Load-Bitmap([string]$path) {
  $source = [System.Drawing.Image]::FromFile($path)
  try { return [System.Drawing.Bitmap]::new($source) } finally { $source.Dispose() }
}

function New-ArgbBitmap([int]$w,[int]$h) {
  return [System.Drawing.Bitmap]::new($w,$h,[System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
}

function New-Graphics([System.Drawing.Bitmap]$bitmap) {
  $g = [System.Drawing.Graphics]::FromImage($bitmap)
  $g.CompositingMode = [System.Drawing.Drawing2D.CompositingMode]::SourceOver
  $g.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
  $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
  $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
  return $g
}

function Resize-Bitmap([System.Drawing.Bitmap]$source,[int]$w,[int]$h) {
  $out = New-ArgbBitmap $w $h
  $g = New-Graphics $out
  try { $g.DrawImage($source,[System.Drawing.Rectangle]::new(0,0,$w,$h)) } finally { $g.Dispose() }
  return $out
}

function Save-Png([System.Drawing.Bitmap]$bitmap,[string]$path) {
  $bitmap.Save($path,[System.Drawing.Imaging.ImageFormat]::Png)
}

function New-Path([object[]]$points) {
  $path = [System.Drawing.Drawing2D.GraphicsPath]::new()
  $pts = [System.Drawing.Point[]]@($points | ForEach-Object { [System.Drawing.Point]::new([int]$_[0],[int]$_[1]) })
  $path.AddPolygon($pts)
  return $path
}

function Draw-CleanPatch([System.Drawing.Graphics]$g,[System.Drawing.Bitmap]$clean,[object[]]$points) {
  $path = New-Path $points
  try {
    $state = $g.Save()
    $g.SetClip($path)
    $g.DrawImage($clean,[System.Drawing.Rectangle]::new(0,$offsetY,$canvasW,1491),0,0,$clean.Width,$clean.Height,[System.Drawing.GraphicsUnit]::Pixel)
    $g.Restore($state)
  } finally { $path.Dispose() }
}

function Draw-CleanEllipse([System.Drawing.Graphics]$g,[System.Drawing.Bitmap]$clean,[int]$x,[int]$y,[int]$w,[int]$h) {
  $path = [System.Drawing.Drawing2D.GraphicsPath]::new()
  try {
    $path.AddEllipse($x,$y + $offsetY,$w,$h)
    $state = $g.Save(); $g.SetClip($path)
    $g.DrawImage($clean,[System.Drawing.Rectangle]::new(0,$offsetY,$canvasW,1491),0,0,$clean.Width,$clean.Height,[System.Drawing.GraphicsUnit]::Pixel)
    $g.Restore($state)
  } finally { $path.Dispose() }
}

function New-MaskedCrop([System.Drawing.Bitmap]$source,[int]$x,[int]$y,[int]$w,[int]$h,[object[]]$points) {
  $out = New-ArgbBitmap $w $h
  $g = New-Graphics $out
  try {
    $g.Clear([System.Drawing.Color]::Transparent)
    $relative = @()
    foreach($pt in $points) {
      $rx = ([int]$pt[0]) - [int]$x
      $ry = ([int]$pt[1]) - [int]$y
      $relative += ,@($rx,$ry)
    }
    $path = New-Path $relative
    try { $g.SetClip($path); $g.DrawImage($source,[System.Drawing.Rectangle]::new(0,0,$w,$h),$x,$y,$w,$h,[System.Drawing.GraphicsUnit]::Pixel) } finally { $path.Dispose() }
  } finally { $g.Dispose() }
  return $out
}

function New-TitleLayer([System.Drawing.Bitmap]$source,[int]$x,[int]$y,[int]$w,[int]$h) {
  $out = New-ArgbBitmap $w $h
  for($yy=0;$yy -lt $h;$yy++) {
    for($xx=0;$xx -lt $w;$xx++) {
      $c = $source.GetPixel($x+$xx,$y+$yy)
      $max = [Math]::Max($c.R,[Math]::Max($c.G,$c.B)); $min=[Math]::Min($c.R,[Math]::Min($c.G,$c.B))
      $cream = ($c.R -gt 205 -and $c.G -gt 188 -and $c.B -gt 160 -and ($max-$min) -lt 72)
      $pink = ($c.R -gt 215 -and $c.B -gt 85 -and $c.G -lt 112 -and ($c.R-$c.G) -gt 105)
      $inCreamWords = (($xx -ge 250 -and $xx -le 930 -and $yy -le 225) -or ($xx -le 1009 -and $yy -ge 105 -and $yy -le 400))
      $inUnderline = ($xx -ge 395 -and $xx -le 1009 -and $yy -ge 250 -and $yy -le 420)
      if(($cream -and $inCreamWords) -or ($pink -and $inUnderline)){ $out.SetPixel($xx,$yy,[System.Drawing.Color]::FromArgb(255,$c.R,$c.G,$c.B)) }
    }
  }
  return $out
}

function New-WingLayer([System.Drawing.Bitmap]$source,[int]$x,[int]$y,[int]$w,[int]$h,[object[]]$points) {
  $out=New-MaskedCrop $source $x $y $w $h $points
  for($yy=0;$yy -lt $h;$yy++){
    for($xx=0;$xx -lt $w;$xx++){
      $c=$out.GetPixel($xx,$yy)
      if($c.A -eq 0){continue}
      $pinkCloud=($c.R -gt 170 -and $c.B -gt 120 -and $c.G -gt 95 -and ($c.R-$c.G) -gt 45)
      $blueCloth=($c.B -gt $c.R -and $c.B -gt $c.G)
      if($pinkCloud -or $blueCloth){$out.SetPixel($xx,$yy,[System.Drawing.Color]::Transparent)}
    }
  }
  return $out
}

function New-CupidBody([System.Drawing.Bitmap]$source,[System.Drawing.Bitmap]$background,[int]$x,[int]$y,[int]$w,[int]$h,[object[]]$points) {
  $out=New-ArgbBitmap $w $h
  $g=New-Graphics $out
  try{
    $g.Clear([System.Drawing.Color]::Transparent)
    $path=[System.Drawing.Drawing2D.GraphicsPath]::new()
    try{
      $trumpet=[System.Drawing.Point[]]@(
        [System.Drawing.Point]::new(24,55),[System.Drawing.Point]::new(67,29),[System.Drawing.Point]::new(88,45),
        [System.Drawing.Point]::new(169,91),[System.Drawing.Point]::new(164,113),[System.Drawing.Point]::new(82,78),
        [System.Drawing.Point]::new(35,91))
      $figure=[System.Drawing.Point[]]@(
        [System.Drawing.Point]::new(104,90),[System.Drawing.Point]::new(136,80),[System.Drawing.Point]::new(150,57),
        [System.Drawing.Point]::new(176,37),[System.Drawing.Point]::new(214,35),[System.Drawing.Point]::new(239,55),
        [System.Drawing.Point]::new(250,88),[System.Drawing.Point]::new(241,114),[System.Drawing.Point]::new(224,132),
        [System.Drawing.Point]::new(238,160),[System.Drawing.Point]::new(246,187),[System.Drawing.Point]::new(270,194),
        [System.Drawing.Point]::new(286,177),[System.Drawing.Point]::new(316,180),[System.Drawing.Point]::new(346,201),
        [System.Drawing.Point]::new(371,226),[System.Drawing.Point]::new(374,269),[System.Drawing.Point]::new(365,306),
        [System.Drawing.Point]::new(374,335),[System.Drawing.Point]::new(360,357),[System.Drawing.Point]::new(338,350),
        [System.Drawing.Point]::new(320,325),[System.Drawing.Point]::new(299,304),[System.Drawing.Point]::new(270,279),
        [System.Drawing.Point]::new(235,264),[System.Drawing.Point]::new(205,236),[System.Drawing.Point]::new(184,206),
        [System.Drawing.Point]::new(172,176),[System.Drawing.Point]::new(150,171),[System.Drawing.Point]::new(125,160),
        [System.Drawing.Point]::new(108,141))
      $path.AddPolygon($trumpet);$path.AddPolygon($figure)
      $g.SetClip($path)
      $g.DrawImage($source,[System.Drawing.Rectangle]::new(0,0,$w,$h),$x,$y,$w,$h,[System.Drawing.GraphicsUnit]::Pixel)
    }finally{$path.Dispose()}
  }finally{$g.Dispose()}

  # Restore the separated blue ribbons by color, without bringing back cloud or gold-frame pixels.
  for($yy=150;$yy -lt [Math]::Min(325,$h);$yy++){
    for($xx=80;$xx -lt $w;$xx++){
      $c=$source.GetPixel($x+$xx,$y+$yy)
      if($c.B -gt ($c.R*1.08) -and $c.B -gt ($c.G*1.12)){$out.SetPixel($xx,$yy,[System.Drawing.Color]::FromArgb(255,$c.R,$c.G,$c.B))}
    }
  }
  for($yy=0;$yy -lt $h;$yy++){
    for($xx=0;$xx -lt $w;$xx++){
      $c=$out.GetPixel($xx,$yy)
      if($c.A -gt 0 -and $c.G -gt ($c.R*1.12) -and $c.G -gt ($c.B*1.1)){$out.SetPixel($xx,$yy,[System.Drawing.Color]::Transparent)}
    }
  }
  return $out
}

function New-StatueLayer([System.Drawing.Bitmap]$source,[int]$x,[int]$y,[int]$w,[int]$h,[object[]]$points) {
  $out=New-MaskedCrop $source $x $y $w $h $points
  for($yy=0;$yy -lt $h;$yy++){
    for($xx=0;$xx -lt $w;$xx++){
      $c=$out.GetPixel($xx,$yy)
      if($c.A -eq 0){continue}
      $greenScore=$c.G-[Math]::Max($c.R,$c.B)
      $darkTeal=($c.R -lt 48 -and $c.G -lt 78 -and $c.B -lt 64 -and $c.G -ge $c.R)
      if($greenScore -ge 18 -or $darkTeal){
        $out.SetPixel($xx,$yy,[System.Drawing.Color]::Transparent)
      }elseif($greenScore -gt 7){
        $alpha=[int](255*(18-$greenScore)/11)
        $out.SetPixel($xx,$yy,[System.Drawing.Color]::FromArgb($alpha,$c.R,$c.G,$c.B))
      }
    }
  }
  return $out
}

function New-GlobeFrame([System.Drawing.Bitmap]$source,[int]$x,[int]$y,[int]$w,[int]$h) {
  $poly = @(@(755,895),@(1045,880),@(1054,1375),@(930,1410),@(790,1340),@(745,1120))
  $out = New-MaskedCrop $source $x $y $w $h $poly
  $cx=925-$x; $cy=1095-$y; $r=145
  for($yy=0;$yy -lt $h;$yy++){
    for($xx=0;$xx -lt $w;$xx++){
      $dx=$xx-$cx; $dy=$yy-$cy
      if(($dx*$dx+$dy*$dy) -lt ($r*$r)){
        $c=$out.GetPixel($xx,$yy)
        $gold=($c.A -gt 0 -and $c.R -gt 80 -and $c.G -gt 50 -and ($c.R-$c.B) -gt 35 -and ($c.R-$c.G) -gt 10)
        if(-not $gold){$out.SetPixel($xx,$yy,[System.Drawing.Color]::Transparent)}
      }
    }
  }
  return $out
}

function Save-Double([string]$path) {
  $src=Load-Bitmap $path
  try { $double=Resize-Bitmap $src ($src.Width*2) ($src.Height*2); try { Save-Png $double ([IO.Path]::Combine([IO.Path]::GetDirectoryName($path),([IO.Path]::GetFileNameWithoutExtension($path)+'@2x.png'))) } finally {$double.Dispose()} } finally {$src.Dispose()}
}

$ref = Load-Bitmap $refPath
$cleanRaw = Load-Bitmap $cleanPath
$clean = Resize-Bitmap $cleanRaw $canvasW 1491
$cleanRaw.Dispose()

# Build the opaque 1055 x 2293 plate, with mirrored edge outpaint and clean-patch replacements.
$base = New-ArgbBitmap $canvasW $canvasH
$topRaw=Load-Bitmap (Join-Path $coverRoot '_generated-top-extension.png');$topTexture=Resize-Bitmap $topRaw $canvasW $offsetY;$topRaw.Dispose()
$bottomRaw=Load-Bitmap (Join-Path $coverRoot '_generated-bottom-extension.png');$bottomTexture=Resize-Bitmap $bottomRaw $canvasW $offsetY;$bottomRaw.Dispose()
$g = New-Graphics $base
try {
  $g.Clear([System.Drawing.Color]::FromArgb(255,7,54,44))
  $g.DrawImage($topTexture,[System.Drawing.Rectangle]::new(0,0,$canvasW,$offsetY))
  $g.DrawImage($ref,[System.Drawing.Rectangle]::new(0,$offsetY,$canvasW,1491))
  $g.DrawImage($bottomTexture,[System.Drawing.Rectangle]::new(0,$offsetY+1491,$canvasW,$offsetY))

  Draw-CleanPatch $g $clean @(@(395,416),@(740,416),@(748,722),@(390,722))
  Draw-CleanPatch $g $clean @(@(175,401),@(445,401),@(450,710),@(175,710))
  Draw-CleanPatch $g $clean @(@(0,720),@(1025,720),@(1025,1210),@(0,1210))
  Draw-CleanPatch $g $clean @(@(235,1055),@(840,1055),@(845,1430),@(230,1430))
  Draw-CleanPatch $g $clean @(@(0,1160),@(350,1160),@(350,1525),@(0,1525))
  Draw-CleanPatch $g $clean @(@(0,1450),@(340,1450),@(340,1635),@(0,1635))
  Draw-CleanPatch $g $clean @(@(680,960),@(1055,960),@(1055,1350),@(680,1350))
  Draw-CleanPatch $g $clean @(@(408,1438),@(735,1438),@(735,1489),@(408,1489))
  Draw-CleanPatch $g $clean @(@(408,1507),@(735,1507),@(735,1559),@(408,1559))
  Draw-CleanPatch $g $clean @(@(408,1578),@(735,1578),@(735,1630),@(408,1630))
  Draw-CleanEllipse $g $clean 780 940 290 310
  Draw-CleanEllipse $g $clean 533 1047 16 16
} finally { $g.Dispose() }

# 120px smoothstep top seam: use the clean edit so the original crown/halo cannot leak into the extension.
$feather=120
for($t=0;$t -lt $feather;$t++){
  $linear=$t/($feather-1.0);$a=$linear*$linear*(3-2*$linear)
  for($xx=0;$xx -lt $canvasW;$xx++){
    $extTop=$topTexture.GetPixel($xx,$offsetY-$feather+$t);$refTop=$clean.GetPixel($xx,$feather-1-$t)
    $tr=[int]($extTop.R*(1-$a)+$refTop.R*$a);$tg=[int]($extTop.G*(1-$a)+$refTop.G*$a);$tb=[int]($extTop.B*(1-$a)+$refTop.B*$a)
    $base.SetPixel($xx,$offsetY-$feather+$t,[System.Drawing.Color]::FromArgb(255,$tr,$tg,$tb))
  }
}

# Remove the tiny gold fleck left at the top-extension join while retaining the velvet fold beneath it.
for($yy=398;$yy -le 430;$yy++){
  for($xx=586;$xx -le 618;$xx++){
    $nx=($xx-602)/16.0;$ny=($yy-414)/16.0;$radius=[Math]::Sqrt($nx*$nx+$ny*$ny)
    if($radius -lt 1){
      $linear=1-$radius;$weight=$linear*$linear*(3-2*$linear)
      $dst=$base.GetPixel($xx,$yy);$src=$base.GetPixel($xx-72,$yy)
      $rr=[int]($dst.R*(1-$weight)+$src.R*$weight);$gg=[int]($dst.G*(1-$weight)+$src.G*$weight);$bb=[int]($dst.B*(1-$weight)+$src.B*$weight)
      $base.SetPixel($xx,$yy,[System.Drawing.Color]::FromArgb(255,$rr,$gg,$bb))
    }
  }
}

# Remove the information-panel grey dot with a broad feathered clone from clean cream paper to its right.
# Sampling on the same scanline preserves the fine paper grain and the horizontal gold rule.
for($yy=1427;$yy -le 1483;$yy++){
  for($xx=512;$xx -le 568;$xx++){
    $nx=($xx-540)/28.0;$ny=($yy-1455)/28.0;$radius=[Math]::Sqrt($nx*$nx+$ny*$ny)
    if($radius -lt 1){
      $linear=1-$radius;$weight=$linear*$linear*(3-2*$linear)
      $dst=$base.GetPixel($xx,$yy);$src=$base.GetPixel($xx+92,$yy)
      $rr=[int]($dst.R*(1-$weight)+$src.R*$weight);$gg=[int]($dst.G*(1-$weight)+$src.G*$weight);$bb=[int]($dst.B*(1-$weight)+$src.B*$weight)
      $base.SetPixel($xx,$yy,[System.Drawing.Color]::FromArgb(255,$rr,$gg,$bb))
    }
  }
}


# The source note's dot coordinate was approximate; remove its actual higher remnant as well.
for($yy=1407;$yy -le 1447;$yy++){
  for($xx=512;$xx -le 552;$xx++){
    $nx=($xx-532)/20.0;$ny=($yy-1427)/20.0;$radius=[Math]::Sqrt($nx*$nx+$ny*$ny)
    if($radius -lt 1){
      $linear=1-$radius;$weight=$linear*$linear*(3-2*$linear)
      $dst=$base.GetPixel($xx,$yy);$src=$base.GetPixel($xx+110,$yy)
      $rr=[int]($dst.R*(1-$weight)+$src.R*$weight);$gg=[int]($dst.G*(1-$weight)+$src.G*$weight);$bb=[int]($dst.B*(1-$weight)+$src.B*$weight)
      $base.SetPixel($xx,$yy,[System.Drawing.Color]::FromArgb(255,$rr,$gg,$bb))
    }
  }
}

# Final pinpoint pass over the darkest centre of the blemish.
for($yy=1412;$yy -le 1448;$yy++){
  for($xx=526;$xx -le 562;$xx++){
    $nx=($xx-544)/18.0;$ny=($yy-1430)/18.0;$radius=[Math]::Sqrt($nx*$nx+$ny*$ny)
    if($radius -lt 1){
      $linear=1-$radius;$weight=$linear*$linear*(3-2*$linear)
      $dst=$base.GetPixel($xx,$yy);$src=$base.GetPixel($xx+110,$yy)
      $rr=[int]($dst.R*(1-$weight)+$src.R*$weight);$gg=[int]($dst.G*(1-$weight)+$src.G*$weight);$bb=[int]($dst.B*(1-$weight)+$src.B*$weight)
      $base.SetPixel($xx,$yy,[System.Drawing.Color]::FromArgb(255,$rr,$gg,$bb))
    }
  }
}
$topTexture.Dispose();$bottomTexture.Dispose()
Save-Png $base (Join-Path $coverRoot 'base.png')

# Original-pixel layers. Polygon masks stay tight on the animated/revealed edge.
$defs = @()
function Add-Layer([string]$id,[string]$file,[int]$x,[int]$y,[System.Drawing.Bitmap]$bitmap,[hashtable]$extra=@{}) {
  Save-Png $bitmap (Join-Path $coverRoot $file)
  $entry=[ordered]@{id=$id;file=$file;x=$x;y=$y+$offsetY;w=$bitmap.Width;h=$bitmap.Height}
  foreach($k in $extra.Keys){$entry[$k]=$extra[$k]}; $script:defs += $entry
}

$haloRaw=Load-Bitmap $haloSource; $halo=Resize-Bitmap $haloRaw 800 800; $haloRaw.Dispose(); Save-Png $halo (Join-Path $coverRoot 'halo.png')
$defs += [ordered]@{id='halo';file='halo.png';center=@(305,521);displaySize=430}

$statue=New-StatueLayer $clean 0 0 510 720 @(@(0,0),@(365,0),@(398,95),@(372,235),@(430,330),@(505,465),@(505,720),@(0,720)); Add-Layer 'statue' 'statue.png' 0 0 $statue
$plateRaw=Load-Bitmap (Join-Path $coverRoot '_generated-plate-invited.png');$plate=Resize-Bitmap $plateRaw 365 280;$plateRaw.Dispose();Add-Layer 'plate-invited' 'plate-invited.png' 390 15 $plate
$titleRaw=Load-Bitmap (Join-Path $coverRoot '_generated-title.png');$title=Resize-Bitmap $titleRaw 1010 465;$titleRaw.Dispose();Add-Layer 'title' 'title.png' 0 330 $title
$togetherRaw=Load-Bitmap (Join-Path $coverRoot '_generated-plate-together.png');$together=Resize-Bitmap $togetherRaw 605 370;$togetherRaw.Dispose();Add-Layer 'plate-together' 'plate-together.png' 235 660 $together
$shipRaw=Load-Bitmap (Join-Path $coverRoot '_generated-ship.png');$ship=Resize-Bitmap $shipRaw 350 370;$shipRaw.Dispose();Add-Layer 'ship' 'ship.png' 0 760 $ship
$wavesRaw=Load-Bitmap (Join-Path $coverRoot '_generated-waves.png');$waves=Resize-Bitmap $wavesRaw 345 195;$wavesRaw.Dispose();Add-Layer 'waves' 'waves.png' 0 1040 $waves
$cupidBody=New-CupidBody $ref $clean 680 575 375 360 @(@(700,642),@(860,600),@(915,605),@(955,630),@(975,690),@(1055,735),@(1055,895),@(935,920),@(850,858),@(790,835),@(760,770),@(705,700)); Add-Layer 'cupid-body' 'cupid-body.png' 680 575 $cupidBody
$wingRaw=Load-Bitmap (Join-Path $coverRoot '_generated-cupid-wing.png');$cupidWing=Resize-Bitmap $wingRaw 165 110;$wingRaw.Dispose();Add-Layer 'cupid-wing' 'cupid-wing.png' 890 610 $cupidWing @{pivot=@(900,1066)}
$frameRaw=Load-Bitmap (Join-Path $coverRoot '_generated-globe-frame.png');$frameScaled=Resize-Bitmap $frameRaw 310 420;$frameRaw.Dispose();$globeFrame=New-ArgbBitmap 310 540;$fg=New-Graphics $globeFrame;try{$fg.Clear([System.Drawing.Color]::Transparent);$fg.DrawImage($frameScaled,0,20,310,420)}finally{$fg.Dispose();$frameScaled.Dispose()};Add-Layer 'globe-frame' 'globe-frame.png' 745 870 $globeFrame @{sphere=[ordered]@{cx=900;cy=1460;r=130}}

# Normalize and harden the seamless globe texture.
$mapRaw=Load-Bitmap $mapSource; $map=Resize-Bitmap $mapRaw 2048 1024; $mapRaw.Dispose()
for($yy=0;$yy -lt 1024;$yy++){
  for($xx=0;$xx -lt 64;$xx++){
    $a=$map.GetPixel($xx,$yy);$b=$map.GetPixel(2047-$xx,$yy)
    $r=[int](($a.R+$b.R)/2);$gg=[int](($a.G+$b.G)/2);$bb=[int](($a.B+$b.B)/2);$c=[System.Drawing.Color]::FromArgb(255,$r,$gg,$bb)
    $map.SetPixel($xx,$yy,$c);$map.SetPixel(2047-$xx,$yy,$c)
  }
}
Save-Png $map (Join-Path $coverRoot 'globe-map.png')

$manifest=[ordered]@{canvas=[ordered]@{w=$canvasW;h=$canvasH;refOffsetY=$offsetY};layers=$defs}
$manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $coverRoot 'layers.json') -Encoding utf8

# Re-composite for QA.
$composite=[System.Drawing.Bitmap]::new($base)
$cg=New-Graphics $composite
try{
  $cg.DrawImage($halo,[System.Drawing.Rectangle]::new(90,306,430,430))
  foreach($entry in $defs){
    if($entry.id -in @('halo','globe-frame')){continue}
    $img=Load-Bitmap (Join-Path $coverRoot $entry.file)
    try{$cg.DrawImage($img,$entry.x,$entry.y,$entry.w,$entry.h)}finally{$img.Dispose()}
  }
  $spherePath=[System.Drawing.Drawing2D.GraphicsPath]::new();$spherePath.AddEllipse(770,1330,260,260);$state=$cg.Save();$cg.SetClip($spherePath)
  $cg.DrawImage($map,[System.Drawing.Rectangle]::new(770,1330,260,260),[System.Drawing.Rectangle]::new(260,230,1024,1024),[System.Drawing.GraphicsUnit]::Pixel);$cg.Restore($state);$spherePath.Dispose()
  $cg.DrawImage($globeFrame,745,1271,310,540)
}finally{$cg.Dispose()}
Save-Png $composite (Join-Path $coverRoot '_composite.png')
$compositePreview=Resize-Bitmap $composite 400 869
Save-Png $compositePreview (Join-Path $coverRoot '_composite-preview.png')
$compositePreview.Dispose()

# Dedicated halo occlusion check: rotate the halo 15 degrees, then redraw the statue above it.
$haloCheck=[System.Drawing.Bitmap]::new($base)
$hg=New-Graphics $haloCheck
try{
  $state=$hg.Save();$hg.TranslateTransform(305,521);$hg.RotateTransform(15);$hg.DrawImage($halo,[System.Drawing.Rectangle]::new(-215,-215,430,430));$hg.Restore($state)
  $hg.DrawImage($statue,0,401,$statue.Width,$statue.Height)
}finally{$hg.Dispose()}
Save-Png $haloCheck (Join-Path $coverRoot '_halo-check.png')
$haloCheckPreview=Resize-Bitmap $haloCheck 400 869
Save-Png $haloCheckPreview (Join-Path $coverRoot '_halo-check-preview.png')
$haloCheckPreview.Dispose()
$haloCheck.Dispose()

# Pixel-difference image and mean absolute RGB difference for the REF area.
$diff=New-ArgbBitmap $canvasW 1491
[long]$sum=0
for($yy=0;$yy -lt 1491;$yy++){
  for($xx=0;$xx -lt $canvasW;$xx++){
    $a=$ref.GetPixel($xx,$yy);$b=$composite.GetPixel($xx,$yy+$offsetY)
    $d=[Math]::Abs($a.R-$b.R)+[Math]::Abs($a.G-$b.G)+[Math]::Abs($a.B-$b.B);$sum+=$d
    $v=[Math]::Min(255,[int]($d/3*3));$diff.SetPixel($xx,$yy,[System.Drawing.Color]::FromArgb(255,$v,0,[int]($v*.22)))
  }
}
$mean=[Math]::Round($sum/($canvasW*1491*3),3)
Save-Png $diff (Join-Path $coverRoot '_diff.png')

# Layer contact sheet on checkerboard.
$previewW=1200;$cellW=300;$cellH=280;$previewH=840
$preview=New-ArgbBitmap $previewW $previewH;$pg=New-Graphics $preview
try{
  for($y=0;$y -lt $previewH;$y+=20){for($x=0;$x -lt $previewW;$x+=20){$brush=[System.Drawing.SolidBrush]::new($(if((($x/20+$y/20)%2)-eq 0){[System.Drawing.Color]::White}else{[System.Drawing.Color]::LightGray}));$pg.FillRectangle($brush,$x,$y,20,20);$brush.Dispose()}}
  $font=[System.Drawing.Font]::new('Arial',14,[System.Drawing.FontStyle]::Bold);$labelBrush=[System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(230,6,59,49))
  $previewEntries=@($defs)+@([ordered]@{id='globe-map';file='globe-map.png';w=2048;h=1024})
  for($i=0;$i -lt $previewEntries.Count;$i++){
    $e=$previewEntries[$i];$img=Load-Bitmap (Join-Path $coverRoot $e.file);try{$col=$i%4;$row=[Math]::Floor($i/4);$maxW=260;$maxH=220;$scale=[Math]::Min($maxW/$img.Width,$maxH/$img.Height);$dw=[int]($img.Width*$scale);$dh=[int]($img.Height*$scale);$dx=$col*$cellW+(($cellW-$dw)/2);$dy=$row*$cellH+38+(($maxH-$dh)/2);$pg.DrawImage($img,[System.Drawing.Rectangle]::new($dx,$dy,$dw,$dh));$pg.DrawString($e.id,$font,$labelBrush,$col*$cellW+10,$row*$cellH+10)}finally{$img.Dispose()}
  }
  $font.Dispose();$labelBrush.Dispose()
}finally{$pg.Dispose()}
Save-Png $preview (Join-Path $coverRoot '_layers-preview.png')

# 2x deliverables.
$deliverables=@('base.png','plate-invited.png','title.png','plate-together.png','halo.png','statue.png','ship.png','waves.png','cupid-body.png','cupid-wing.png','globe-frame.png','globe-map.png')
foreach($file in $deliverables){Save-Double (Join-Path $coverRoot $file)}

$readme=@'
# Cover layer package

Canvas: **1055 × 2293**, with the original 1055 × 1491 reference at **y = 401**. Coordinates in `layers.json` are 1x canvas coordinates.

## Production notes

- `base.png`: original reference retained outside the removal masks. Removed regions are filled from the imagegen clean-background edit. The invited-plate patch extends below the former crown. The top extension uses a 120px clean-background smoothstep seam; the bottom uses the generated velvet/satin continuation directly so books are not mirrored or vertically smeared. The information-panel dot is replaced with feathered cream-paper texture.
- `cupid-body.png`: cropped from original reference pixels with hand-authored polygon, spatial and color masks to exclude the original wing, gold-frame fragment, velvet and cloud fragments.
- `cupid-wing.png`: reference-guided complete feathered wing extraction with a reconstructed wing root for animation.
- `ship.png`, `waves.png`: reference-guided transparent extractions, used because the original subjects overlap clouds, engraving paper and each other too heavily for a clean animated edge.
- `statue.png`: taken from the clean edit, then polygon and emerald-color masked so the right facial/neck contour is transparent outside the sculpture and cannot block the rotating halo.
- `plate-invited.png`, `plate-together.png`, `globe-frame.png`: reference-guided transparent extractions generated to eliminate visible background chunks during animation.
- `title.png`: reference-guided transparent extraction preserving the exact wording, two-line composition, inset star and hot-pink underline without the cloud/dress contamination produced by color-key extraction.
- `halo.png`: newly generated transparent 360-degree gilded sunburst, normalized to 800 × 800.
- `globe-map.png`: newly generated antique equirectangular texture, normalized to 2048 × 1024; the outer 64px were mirrored/averaged so left and right edges match.
- `@2x` files: Lanczos/high-quality bicubic output from the final 1x files.
- QA: `_composite.png` is rebuilt from `base.png` plus the manifest layers; `_diff.png` compares y=401..1891 against the source reference; `_layers-preview.png` shows isolated transparency; `_halo-check.png` rotates the halo 15 degrees under the statue.

## QA result

Mean absolute RGB difference: **__MEAN__ / 255** per channel.

## Known limitations

- No callable Python interpreter was available, so the required deterministic pixel operations and QA were performed with Windows System.Drawing instead of Python/Pillow.
- Built-in image editing cannot accept the task's exact mask geometry. The clean background was generated once, then inserted only through deterministic masks; this preserves all untouched reference pixels but leaves some generated texture under moving layers.
- The Cupid body retains reference pixels, while the completed wing and globe frame are reference-guided reconstructions; their hidden geometry is approximate rather than a full 3D reconstruction.
- The top/bottom extensions are reference-guided material outpaints. Their far edges intentionally avoid focal objects; the 120px smoothstep feather may still soften tiny edge details.
'@
$readme=$readme.Replace('__MEAN__',[string]$mean)
$readme | Set-Content -LiteralPath (Join-Path $coverRoot 'README.md') -Encoding utf8

$preview.Dispose();$diff.Dispose();$composite.Dispose();$map.Dispose();$globeFrame.Dispose();$cupidWing.Dispose();$cupidBody.Dispose();$waves.Dispose();$ship.Dispose();$together.Dispose();$title.Dispose();$plate.Dispose();$statue.Dispose();$halo.Dispose();$base.Dispose();$clean.Dispose();$ref.Dispose()
Write-Output "Built cover layer package. Mean absolute RGB difference: $mean"
