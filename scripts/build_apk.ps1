param(
    [string]$OutApk = "build\GestorFinanceiro.apk"
)

$ErrorActionPreference = "Stop"

$sdk = if ($env:ANDROID_HOME) { $env:ANDROID_HOME } else { "$env:LOCALAPPDATA\Android\Sdk" }
$btDir = Get-ChildItem "$sdk\build-tools" -Directory | Sort-Object Name -Descending | Select-Object -First 1
if (-not $btDir) { throw "Android build-tools não encontrado em $sdk\build-tools" }
$bt = $btDir.FullName

$androidJar = "$sdk\platforms\android-34\android.jar"
if (-not (Test-Path $androidJar)) { throw "android.jar (API 34) não encontrado em $androidJar" }

$jdkBin = $null
$jdkCandidates = Get-ChildItem "C:\Program Files\Java" -Directory -ErrorAction SilentlyContinue | Sort-Object Name -Descending
foreach ($c in $jdkCandidates) {
    if ((Test-Path (Join-Path $c.FullName "bin\keytool.exe")) -and (Test-Path (Join-Path $c.FullName "bin\javac.exe"))) {
        $jdkBin = Join-Path $c.FullName "bin"
        break
    }
}
if (-not $jdkBin) { throw "JDK com javac.exe e keytool.exe não encontrado em C:\Program Files\Java" }

$root = Split-Path -Parent $PSScriptRoot
Push-Location $root

try {
    Remove-Item -Recurse -Force build\compiled_res, build\classes, build\dex, build\out, build\assets -ErrorAction SilentlyContinue
    New-Item -ItemType Directory -Force -Path build\compiled_res, build\classes, build\dex, build\out, build\assets | Out-Null

    Copy-Item -Recurse -Force www build\assets\www

    Write-Host "1. Compilando recursos..."
    & "$bt\aapt2.exe" compile --dir android\res -o build\compiled_res\res.zip
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "2. Linkando Manifesto e Recursos..."
    & "$bt\aapt2.exe" link -o build\out\unaligned.apk -I $androidJar --manifest android\AndroidManifest.xml --java android\src --auto-add-overlay build\compiled_res\res.zip
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "3. Compilando Java..."
    $javaFiles = Get-ChildItem -Path android\src -Recurse -Filter *.java | ForEach-Object { $_.FullName }
    & "$jdkBin\javac.exe" -source 1.8 -target 1.8 -Xlint:-options -bootclasspath $androidJar -d build\classes $javaFiles
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "4. Gerando classes.dex..."
    $classFiles = Get-ChildItem -Path build\classes -Recurse -Filter *.class | ForEach-Object { $_.FullName }
    & "$bt\d8.bat" --min-api 24 --lib $androidJar --output build\dex $classFiles
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "5. Empacotando classes.dex e assets com barras normais (/)..."
    python -c "
import zipfile, os
with zipfile.ZipFile(r'build\out\unaligned.apk', 'a', zipfile.ZIP_DEFLATED) as z:
    z.write(r'build\dex\classes.dex', 'classes.dex')
    for root, _, files in os.walk('www'):
        for fn in files:
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, 'www').replace(os.sep, '/')
            arcname = 'assets/www/' + rel
            compress = zipfile.ZIP_STORED if fn.lower().endswith('.png') else zipfile.ZIP_DEFLATED
            z.write(full, arcname, compress_type=compress)
"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "6. Alinhando APK (zipalign)..."
    & "$bt\zipalign.exe" -f -p 4 build\out\unaligned.apk build\out\aligned.apk
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    $keystore = "build\local-debug.keystore"
    if (-not (Test-Path $keystore)) {
        Write-Host "7. Gerando keystore local de desenvolvimento..."
        & "$jdkBin\keytool.exe" -genkeypair -v -keystore $keystore -alias gestor -keyalg RSA -keysize 2048 -validity 10000 -storepass dev123456 -keypass dev123456 -dname "CN=GestorFinanceiro, O=LocalBuild, C=BR"
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }

    Write-Host "8. Assinando APK..."
    $outDir = Split-Path -Parent $OutApk
    if ($outDir -and -not (Test-Path $outDir)) { New-Item -ItemType Directory -Force -Path $outDir | Out-Null }
    & "$bt\apksigner.bat" sign --v1-signing-enabled true --v2-signing-enabled true --ks $keystore --ks-pass pass:dev123456 --key-pass pass:dev123456 --ks-key-alias gestor --out $OutApk build\out\aligned.apk
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "9. Verificando assinatura..."
    & "$bt\apksigner.bat" verify --verbose $OutApk
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

    Write-Host "`nAPK gerado com sucesso em: $OutApk"
} finally {
    Pop-Location
}
