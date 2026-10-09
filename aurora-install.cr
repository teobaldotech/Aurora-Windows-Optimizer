```ruby
# frozen_string_literal: true

# ============================================================
# Aurora Installer PRO — correções prioritárias
# Ruby + Windows PowerShell
# ============================================================

require "tempfile"
require "rbconfig"

module AuroraInstaller
  POWERSHELL = "powershell.exe"
  SCRIPT_NAME = "aurora"

  module_function

  def windows?
    RbConfig::CONFIG.fetch("host_os", "").match?(
      /mswin|mingw|cygwin/i
    )
  end

  # Executa um processo sem interpolar argumentos Ruby no shell.
  def execute(*args)
    result = system(*args)
    result == true && $?.success?
  rescue SystemCallError => e
    warn "Falha ao iniciar processo: #{e.message}"
    false
  end

  # Escapa uma string para uso como literal PowerShell.
  def ps_literal(value)
    "'#{value.to_s.gsub("'", "''")}'"
  end

  # Cria um script temporário e solicita elevação pelo UAC.
  def run_as_admin(script)
    Tempfile.create(["aurora_", ".ps1"]) do |file|
      file.write(<<~POWERSHELL)
        $ErrorActionPreference = 'Stop'

        try {
          #{script}
          exit 0
        }
        catch {
          [Console]::Error.WriteLine($_.Exception.Message)
          exit 1
        }
      POWERSHELL

      file.flush

      # Start-Process recebe os argumentos como uma lista
      # de parâmetros PowerShell, evitando interpolação Ruby
      # direta dentro do comando de instalação.
      command = <<~POWERSHELL
        $process = Start-Process `
          -FilePath 'powershell.exe' `
          -Verb RunAs `
          -Wait `
          -PassThru `
          -ArgumentList @(
            '-NoProfile',
            '-ExecutionPolicy',
            'RemoteSigned',
            '-File',
            #{ps_literal(file.path)}
          )

        exit $process.ExitCode
      POWERSHELL

      execute(
        POWERSHELL,
        "-NoProfile",
        "-Command",
        command
      )
    end
  rescue Interrupt
    warn "\nOperação cancelada pelo usuário."
    false
  rescue SystemCallError => e
    warn "Falha no arquivo temporário: #{e.message}"
    false
  end

  # Instala e executa somente após validar o arquivo.
  def install_and_run
    script = <<~POWERSHELL
      if (-not (Get-Command Install-Script -ErrorAction SilentlyContinue)) {
        throw 'Install-Script não está disponível.'
      }

      if (-not (Get-PSRepository -Name 'PSGallery' -ErrorAction SilentlyContinue)) {
        throw 'O repositório PSGallery não está configurado.'
      }

      Write-Host 'Instalando Aurora...' -ForegroundColor Cyan

      Install-Script `
        -Name 'aurora' `
        -Repository 'PSGallery' `
        -Scope AllUsers `
        -Force `
        -ErrorAction Stop

      $installed = Get-InstalledScript `
        -Name 'aurora' `
        -ErrorAction Stop

      if (-not $installed -or
          [string]::IsNullOrWhiteSpace($installed.InstalledLocation)) {
        throw 'Não foi possível validar a instalação.'
      }

      $scriptPath = Join-Path $installed.InstalledLocation 'aurora.ps1'

      if (-not (Test-Path -LiteralPath $scriptPath -PathType Leaf)) {
        throw "Script não encontrado no caminho esperado: $scriptPath"
      }

      Write-Host 'Executando Aurora...' -ForegroundColor Cyan

      & $scriptPath

      if (-not $?) {
        throw 'A execução do Aurora indicou uma falha.'
      }

      Write-Host 'Execução concluída.' -ForegroundColor Green
    POWERSHELL

    puts 'Aurora Installer PRO'
    puts 'Solicitando autorização administrativa...'

    run_as_admin(script)
  end
end

unless AuroraInstaller.windows?
  warn 'Este instalador funciona somente no Windows.'
  exit 1
end

exit(AuroraInstaller.install_and_run ? 0 : 1)
```
