# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.4] - 2025-08-19

### ⚡ Performance Improvements
- **Graph Management Optimization**: Removed redundant `couplesMaked` list and implemented efficient set-based duplicate prevention in `getEdges()` method for faster graph construction
- **Memory Management**: Introduced thread-safe LRU cache system (`LRUImageCache`) with 100MB memory limit for better resource management
- **Algorithm Optimization**: Improved breeding path calculation efficiency by preventing duplicate couple processing

### 🔧 Core System Enhancements
- **Resource Handling**: Enhanced PyInstaller compatibility with improved `resourcePath()` function using `getattr()` for safer MEIPASS access
- **Error Handling**: Added comprehensive exception handling in image loading operations to prevent crashes
- **Graphviz Integration**: Improved PATH configuration and binary detection for better cross-system compatibility
- **Build System**: Updated build script (`build.bat`) with dynamic version retrieval and relative path handling

### 🎨 User Interface & Features  
- **Multi-Language Support**: Expanded internationalization from 3 to 9 languages:
  - Added: German (de), Spanish (es), Japanese (ja), Korean (ko), Portuguese (pt), Russian (ru)
  - Existing: English (en), French (fr), Chinese (ch)
- **Window Management**: Enhanced TreeFrame resizing with debouncing mechanism (150ms delay) for smoother UI performance
- **Configuration System**: Added `locked` parameter support for persistent frame states in tree windows

### 📚 Documentation & Project Structure
- **README Overhaul**: Complete redesign with modern GitHub badges, multi-language sections, and comprehensive feature overview
- **Development Workflow**: Improved build process with automatic version handling
- **Git Configuration**: Updated `.gitignore` to include Claude Code files and build directories

### 🛠️ Technical Improvements
- **Code Quality**: Improved singleton pattern implementation with better initialization handling
- **Cache Management**: Added intelligent cache eviction policies for image storage
- **Thread Safety**: Implemented thread-safe operations for concurrent access scenarios
- **Path Resolution**: Enhanced cross-platform path handling for better compatibility

### 🔄 Data & Configuration
- **Pal Database**: Updated with latest Palworld creatures and breeding combinations
- **Language Files**: Expanded translation coverage across all supported languages
- **Build Configuration**: Streamlined PyInstaller configuration for more reliable executable generation

## [3.0.3] - 2025-08-19

### Added
- Automatic release workflow with GitHub Actions
- Changelog file for tracking changes

### Changed
- Improved project structure and documentation

### Fixed
- Various bug fixes and improvements

## [3.0.0] - 2025-01-29

### Added
- Major version release with comprehensive updates
- New Palworld creatures and breeding combinations
- Chinese language support and localization
- Improved icon system with new creature icons

### Changed
- Enhanced UI finishes and visual improvements
- Updated language management system
- Optimized breeding combination calculations
- Improved code structure and organization

### Fixed
- Fixed multiple breeding combination issues
- Corrected syntax and functionality bugs
- Resolved Chinese language display issues
- Fixed various stability and performance issues

### Removed
- Cleaned up unnecessary Graphviz directories
- Removed redundant build files

## [2.2.0] - 2024-12-27

### Added
- New Palworld creatures added to database
- Updated breeding combinations

### Changed
- Updated README documentation
- Improved gitignore configuration

### Fixed
- Code improvements and bug fixes

## [2.1.5] - 2024-07-31

### Fixed
- Fixed relative path issues
- Corrected Pal breeding combinations
- Resolved blank case handling
- Fixed various stability issues

### Changed
- Cleaned up project structure
- Removed Graphviz folder from repository

## [2.1.0] - 2024-07-15

### Added
- Palworld update preparations
- New icons and visual improvements
- Enhanced optimization algorithms

### Changed
- Screen size adaptability improvements
- Updated button text and UI elements
- Code optimization and comments added
- Icon resizing and visual enhancements

### Fixed
- Fixed only-child breeding bug with optimizations
- Resolved no-connection errors
- Fixed translation corrections
- Various bug fixes and improvements

### Removed
- Cleaned up default configurations

## [1.5.0] - 2024-04-28

### Added
- Initial stable release
- Core breeding tree functionality
- Basic UI implementation
- Fundamental Palworld creature database

### Changed
- Established project foundation
- Basic application structure

### Fixed
- Initial bug fixes and stability improvements