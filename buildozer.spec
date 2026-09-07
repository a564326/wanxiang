[app]

# (str) Title of your application
title = 万象词条录

# (str) Package name
package.name = wanxiang

# (str) Package domain (needed for android/ios)
package.domain = com.wanxiang.tianbang

# (str) Source files to include
source.dir = .
source.include_exts = py,png,jpg,jpeg,json,md
source.exclude_exts = spec,sh,bat

# (list) Application version
version = 0.2

# (str) Application icon
icon.filename = assets/icon.png

# (str) Supported orientation
orientation = portrait

# (bool) Show status bar
fullscreen = 0

[buildozer]

# (int) Log level (0 = minimal, 1 = normal, 2 = verbose)
log_level = 1

# (str) Android NDK directory
android.ndk = 26b

# (bool) Android x86 support
android.archs = arm64-v8a, armeabi-v7a

# (int) Android API
android.api = 34
android.minapi = 21
android.targetapi = 34

# (str) Android SDK build tools
android.build_tools = 34.0.0

# (bool) Automatically accept SDK license
android.accept_sdk_license = True

# (str) Gradle dependency resolution
android.gradle_dependencies = androidx.appcompat:appcompat:1.6.1

# Python for android requirements
requirements = python3,kivy==2.3.1,pillow

# (str) Extra Java compile options
android.add_compile_options = -source 8 -target 8

# (list) Permissions
android.permissions = INTERNET

# (bool) Strip debug symbols
android.strip_debug = True
