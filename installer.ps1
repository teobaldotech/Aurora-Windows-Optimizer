# Check if you are running as administrator
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Running as a non-administrator. Requesting elevation..."

    # Request elevation to administrator
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$($MyInvocation.MyCommand.Path)`"" -Verb RunAs
    exit
}

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

function Show-FolderBrowserDialog {
    $folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
    $folderBrowser.Description = "Select the installation folder for Aurora Windows Optimizer"
    
    if ($folderBrowser.ShowDialog() -eq 'OK') {
        $textBox.Text = $folderBrowser.SelectedPath
    }
}

function Update-UI {
    param([int]$Percent)
    $progressBar.Value = $Percent
    [System.Windows.Forms.Application]::DoEvents()
}

function Install-AuroraWindowsOptimizer {
    if (-not $textBox.Text -or -not (Test-Path $textBox.Text)) {
        [System.Windows.Forms.MessageBox]::Show("Please select a valid folder before installing.", "Error", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
        return
    }

    $buttonInstall.Enabled = $false
    $buttonFolder.Enabled = $false

    try {
        Update-UI -Percent 10

        # Set variables
        $repo = "azurejoga/Aurora-Windows-Optimizer"
        $file = "Aurora-Windows-Optimizer.zip"
        $targetDir = $textBox.Text
        $tempZipPath = Join-Path [System.IO.Path]::GetTempPath() $file
        $shortcutName = "Aurora Windows Optimizer"

        # Determine the latest release
        $releases = "https://api.github.com/repos/$repo/releases"
        $tag = (Invoke-WebRequest -Uri $releases -UseBasicParsing | ConvertFrom-Json)[0].tag_name

        Update-UI -Percent 30

        # Download the zip file to temp directory
        $download = "https://github.com/$repo/releases/download/$tag/$file"
        Invoke-WebRequest -Uri $download -OutFile $tempZipPath -UseBasicParsing

        Update-UI -Percent 60

        # Extract the contents of the zip file
        Expand-Archive -Path $tempZipPath -DestinationPath $targetDir -Force

        Update-UI -Percent 80

        # Create a shortcut on the desktop using WScript.Shell
        $shell = New-Object -ComObject WScript.Shell
        $executablePath = Join-Path $targetDir "aurora-windows-optimizer\aurora windows optimizer.exe"
        $shortcutPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), "$shortcutName.lnk")

        if (Test-Path $shortcutPath) {
            Remove-Item $shortcutPath -Force
        }

        $shortcut = $shell.CreateShortcut($shortcutPath)
        $shortcut.TargetPath = $executablePath
        $shortcut.WorkingDirectory = Join-Path $targetDir "aurora-windows-optimizer"
        $shortcut.Save()

        # Clean up temporary downloaded file
        if (Test-Path $tempZipPath) {
            Remove-Item $tempZipPath -Force
        }

        Update-UI -Percent 100

        [System.Windows.Forms.MessageBox]::Show("The latest release of Aurora Windows Optimizer has been successfully downloaded and installed.", "Installation Complete", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
    }
    catch {
        Update-UI -Percent 0
        [System.Windows.Forms.MessageBox]::Show("An error occurred during installation:`n$($_.Exception.Message)", "Installation Failed", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
    }
    finally {
        $buttonInstall.Enabled = $true
        $buttonFolder.Enabled = $true
    }
}

# Create the main window
$form = New-Object System.Windows.Forms.Form
$form.Text = "Aurora Windows Optimizer Installer"
$form.Size = New-Object System.Drawing.Size(420, 220)
$form.StartPosition = "CenterScreen"
$form.FormBorderStyle = [System.Windows.Forms.FormBorderStyle]::FixedDialog
$form.MaximizeBox = $false

# Create a text box to display the folder path
$textBox = New-Object System.Windows.Forms.TextBox
$textBox.Location = New-Object System.Drawing.Point(30, 20)
$textBox.Size = New-Object System.Drawing.Size(340, 20)

# Create a button to open the folder selector
$buttonFolder = New-Object System.Windows.Forms.Button
$buttonFolder.Location = New-Object System.Drawing.Point(30, 55)
$buttonFolder.Size = New-Object System.Drawing.Size(160, 30)
$buttonFolder.Text = "Browse Folder..."
$buttonFolder.Add_Click({ Show-FolderBrowserDialog })

# Create a button to install
$buttonInstall = New-Object System.Windows.Forms.Button
$buttonInstall.Location = New-Object System.Drawing.Point(210, 55)
$buttonInstall.Size = New-Object System.Drawing.Size(160, 30)
$buttonInstall.Text = "Install"
$buttonInstall.Add_Click({ Install-AuroraWindowsOptimizer })

# Create a progress bar
$progressBar = New-Object System.Windows.Forms.ProgressBar
$progressBar.Location = New-Object System.Drawing.Point(30, 105)
$progressBar.Size = New-Object System.Drawing.Size(340, 23)
$progressBar.Style = [System.Windows.Forms.ProgressBarStyle]::Continuous

# Add controls to the main window
$form.Controls.Add($textBox)
$form.Controls.Add($buttonFolder)
$form.Controls.Add($buttonInstall)
$form.Controls.Add($progressBar)

# Show the window
$form.ShowDialog()
