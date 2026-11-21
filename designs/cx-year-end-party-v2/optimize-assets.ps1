Add-Type -AssemblyName System.Drawing

$assetRoot = Join-Path $PSScriptRoot 'assets'

function Resize-Image([string]$source, [string]$destination, [int]$maxWidth, [bool]$jpeg) {
  $image = [System.Drawing.Image]::FromFile($source)
  try {
    $width = [Math]::Min($maxWidth, $image.Width)
    $height = [int][Math]::Round($image.Height * ($width / $image.Width))
    $format = if ($jpeg) { [System.Drawing.Imaging.PixelFormat]::Format24bppRgb } else { [System.Drawing.Imaging.PixelFormat]::Format32bppArgb }
    $bitmap = New-Object System.Drawing.Bitmap($width, $height, $format)
    try {
      $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
      try {
        $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
        $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
        if ($jpeg) { $graphics.Clear([System.Drawing.Color]::White) } else { $graphics.Clear([System.Drawing.Color]::Transparent) }
        $graphics.DrawImage($image, 0, 0, $width, $height)
      } finally { $graphics.Dispose() }
      if ($jpeg) {
        $codec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object MimeType -eq 'image/jpeg'
        $parameters = New-Object System.Drawing.Imaging.EncoderParameters(1)
        $parameters.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, [long]82)
        $bitmap.Save($destination, $codec, $parameters)
        $parameters.Dispose()
      } else { $bitmap.Save($destination, [System.Drawing.Imaging.ImageFormat]::Png) }
    } finally { $bitmap.Dispose() }
  } finally { $image.Dispose() }
}

'statue','ship','angel','globe' | ForEach-Object {
  Resize-Image (Join-Path $assetRoot "cover-$_.png") (Join-Path $assetRoot "cover-$_.web.png") 650 $false
}

'dolphin','rose','star','eagle' | ForEach-Object {
  Resize-Image (Join-Path $assetRoot "look-$_.png") (Join-Path $assetRoot "look-$_.web.jpg") 720 $true
}

'fashionista','snack-strategist','joke-cracker','ai-master','best-listener','best-dressed','winning-team' | ForEach-Object {
  Resize-Image (Join-Path $assetRoot "award-$_.png") (Join-Path $assetRoot "award-$_.web.jpg") 600 $true
}

'trax','flora' | ForEach-Object {
  Resize-Image (Join-Path $assetRoot "venue-$_-baroque.png") (Join-Path $assetRoot "venue-$_-baroque.web.jpg") 900 $true
}
