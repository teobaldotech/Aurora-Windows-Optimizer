# 🌌 Aurora Windows Optimizer

**Transform your Windows PC with customizable optimization tools.** 💻

Aurora Windows Optimizer is an open-source application designed to help users customize Windows, manage system features, perform maintenance tasks, and apply optimization commands through a single interface.

Whether your goal is to adjust system settings, reduce unwanted components, improve accessibility, or manage privacy-related options, Aurora provides a collection of commands that you can customize according to your needs.

Special thanks to [edu-mx](https://github.com/edu-mx) for contributing to the development of this project. 🙌

## ✨ Features

Aurora offers a customizable collection of Windows commands and utilities.

### 🛠️ Command Management

- **Custom commands:** Add your own commands and adapt Aurora to your workflow.
- **Flexible organization:** Edit, remove, reorder, and sort commands alphabetically.
- **Simplified updates:** Check for application updates directly from Aurora.
- **Execution notifications:** Receive notifications when commands complete successfully or encounter errors.
- **Change log access:** View project changes directly from the application.
- **Restoration points:** Create Windows System Restore points before applying changes, where supported.

### ⚡ System Optimization and Maintenance

Available commands and utilities include:

- Clear the Windows DNS cache.
- Manage Windows animations and selected system settings.
- Clean browser caches and perform disk maintenance.
- Apply network-related adjustments using native Windows commands.
- Manage preinstalled Windows applications.
- Configure Windows Update behavior.
- Manage selected Windows telemetry and privacy settings.
- Access more than 100 optimization commands, according to the project's feature list.

**Important:** Results depend on your Windows version, hardware, configuration, and the commands you choose. Not every optimization produces a measurable performance improvement.

### 📦 Application Installation and System Utilities

Aurora's listed utilities include options to install or manage:

1. NVDA screen reader for users who are blind or have low vision.
2. Microsoft Visual C++ Redistributable packages.
3. .NET Framework and related .NET components.
4. Java 8 JDK.
5. WinRAR or 7-Zip.
6. DirectPlay for compatible legacy games.
7. Visual Studio Code.
8. TeamViewer.
9. Classic Start menu or Task Manager alternatives.
10. Additional Windows utilities and components.

The availability and compatibility of individual packages may vary. Check each application's official requirements before installation.

### 🔐 Privacy and Security Controls

Aurora includes commands for managing selected Windows security and privacy features, such as:

- Windows Defender settings.
- Windows Firewall settings.
- Windows telemetry options.
- Automatic Windows sign-in.
- Windows 11 Recall availability or settings, where supported.

**Security warning:** Disabling Microsoft Defender, the Windows Firewall, Windows Update, or other protective features can expose your computer to malware, unauthorized access, and security vulnerabilities. Automatic sign-in can also expose your account to anyone with physical access to your device.

Only change these settings when you understand the consequences and have an appropriate alternative protection strategy.

### ♿ Accessibility

Aurora is designed to support visually impaired users, including keyboard-oriented workflows and accessibility features.

The project also lists NVDA-related functionality. Actual accessibility depends on the application's current implementation and the compatibility of its interface with screen readers.

### 🌐 Community and Open Source

- Review and contribute to the source code.
- Report bugs and request improvements through GitHub Issues.
- Share ideas and custom commands with the community.
- Submit benchmark information to help document optimization results.
- Review the project's change log and installation instructions.

## 🖥️ Is Aurora Safe?

Aurora is an open-source project, but **no optimizer should be considered completely safe solely because it is open source, digitally signed, or has been scanned by an antivirus service.**

Before running Aurora, follow these precautions:

1. **Download from trusted sources.** Use the official [GitHub repository](https://github.com/azurejoga/Aurora-Windows-Optimizer) or the project's documented Chocolatey distribution.
2. **Review antivirus results.** Check the [Aurora VirusTotal report](https://www.virustotal.com/gui/file/21addd102f59240bfc9689f01ef4c70a8ce617893f688ebc98b53de1225afb8a/summary). Antivirus results are useful indicators, but they do not guarantee that a file is harmless.
3. **Verify file hashes.** Compare the downloaded file's SHA-256 hash with a value published through a trusted, independent project source.
4. **Check the digital signature.** Verify the publisher, certificate validity, and signature integrity. A valid signature identifies the signer and helps detect modifications; it does not prove that every operation is safe.
5. **Inspect commands before execution.** Custom commands can modify system settings, remove applications, or make administrative changes.
6. **Create a backup.** Back up important files and create a Windows System Restore point before making significant system changes.

Never execute an installer or archive if its integrity cannot be verified or its origin is uncertain.

## 💾 Installation

Follow the installation instructions maintained by the project:

- [Installation methods](https://github.com/azurejoga/Aurora-Windows-Optimizer/blob/aurora/instalation.md)
- [Official GitHub repository](https://github.com/azurejoga/Aurora-Windows-Optimizer)

Use only the distribution methods documented by the project and verify downloads before running them.

## 🚀 How to Use Aurora

1. Download and install Aurora using a documented installation method.
2. Open the application and review its initial instructions.
3. Create a Windows System Restore point and back up important data before applying changes.
4. Browse the available optimization commands.
5. Read each command's description and understand its effects before executing it.
6. Select a command and press **Enter**, following the application's on-screen instructions.
7. Customize the command list by editing, adding, removing, or rearranging entries as needed.
8. Restart Windows when a command requires it, then check whether the intended change was successful.

**Recommendation:** Apply changes individually rather than running every optimization at once. This makes troubleshooting easier if something stops working.

## 🔄 Updating Aurora

To check for updates:

1. Open Aurora.
2. Press **Alt** or open the **Tools** menu.
3. Select **Check for Updates**.
4. Follow the installer instructions.
5. Select the correct installation directory when prompted.

Depending on the installation method, Aurora may be located in a user-selected directory or a package-manager-managed location.

The NVDA add-on may be stored in the `Documents` folder, depending on your configuration. Do not assume that every installation uses the same directory.

For additional details, consult the [installation guide](https://github.com/azurejoga/Aurora-Windows-Optimizer/blob/aurora/instalation.md).

## 📝 Change Log

Review recent changes, fixes, and feature additions:

[View the Aurora change log](https://github.com/azurejoga/Aurora-Windows-Optimizer/blob/aurora/changelog.md)

## 🐞 Bug Reports and Contributions

Found a bug or have an idea for improvement?

1. Visit the [Aurora GitHub repository](https://github.com/azurejoga/Aurora-Windows-Optimizer).
2. Review existing issues to avoid duplicates.
3. Open a new issue with a clear description of the problem.
4. Include your Windows version, relevant logs, reproduction steps, and expected behavior when available.

Contributions are welcome. Please review the repository's contribution guidelines before submitting changes, if available.

## ⚠️ Disclaimer

Aurora Windows Optimizer modifies Windows settings and may execute commands with elevated privileges. Incorrect configuration or incompatible commands can cause system instability, loss of functionality, or data loss.

- Use the application at your own risk.
- Review commands before executing them.
- Keep backups of important data.
- Do not disable security features without understanding the risks.
- Test significant changes in a controlled environment whenever possible.

The maintainers' actual responsibilities and any applicable warranties are governed by the project's license and relevant law.

## 📄 License

Aurora Windows Optimizer is distributed under the [MIT License](https://opensource.org/license/mit/).

See the repository's `LICENSE` file for the complete license text.

---

**Thank you for checking out Aurora Windows Optimizer!** 🌌

Explore the project, review the available commands, and contribute to making Windows customization more accessible and transparent.
