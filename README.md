## HostLoca XAMPP Controller
HostLoca is an open source Python desktop application that makes working with XAMPP easier and more reliable. XAMPP is widely used for local development but it often creates problems when reinstalling, importing databases, or managing user credentials. HostLoca was built to solve these issues by automating backups, simplifying database imports, and allowing developers to set up custom superusers that match production environments.

## Description
HostLoca provides a smarter way to manage your XAMPP environment. It allows you to keep your projects safe in a custom HTDOCS folder outside XAMPP, automatically import SQL and SQL GZ files into MySQL, and configure unique superusers alongside the default accounts. This makes backups faster, database management simpler, and switching between local and production credentials much smoother.

## Features
Custom HTDOCS folder outside XAMPP for lightweight backups and quick reinstalls  
Automatic import of SQL and SQL GZ files directly into MySQL without manual phpMyAdmin steps  
Superuser setup with unique username and password alongside root, pma, and 127.0.0.0 accounts  
Production aware configuration that allows quick switching of credentials  

## Getting Started
### Prerequisites
Python 3.8 or higher  
XAMPP installed on your system  
MySQL enabled in XAMPP  

### Installation
Clone the repository  
```
git clone https://github.com/bmwtch/HostLoca---XAMPP-Controller.git
cd HostLoca---XAMPP-Controller
python main.py
```

### Windows Desktop Version
A packaged installer for Windows : https://github.com/bmwtch/HostLoca---XAMPP-Controller/releases/tag/v1.0.0

### Linux Support
Linux packaging is planned but not yet available. Contributions from the community are welcome to help create AppImage, deb, or Flatpak packages.

## Roadmap
Windows installer  
Linux packaging  
Support for multiple databases such as MariaDB and PostgreSQL  
Project templates for frameworks like WordPress and Laravel  
Environment profiles for development, staging, and production  

## Contributing
Contributions are welcome. Fork the repository, create a feature branch, and submit a pull request. Check the issues tab for tasks marked as good first issue if you are new to open source.

## Support
If this project saves you time or effort you can support development by using the donate button included in the application. Starring the repository also helps spread the word.

## Community
Blog post and Reddit announcement will be shared soon. Updates will be posted regularly in developer communities.

## License
This project is licensed under the MIT License. You are free to use, modify, and distribute it.
