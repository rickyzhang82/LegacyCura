%global _curaName      __curaName__
%global _baseDir       __basedir__
%global _version       __version__
%global _gitCura       __gitCura__
%global _gitCuraEngine __gitCuraEngine__
%global _gitPower      __gitPower__
%global debug_package %{nil}

Name:             %{_curaName}
Version:          %{_version}
Release:          1%{?dist}
Summary:          3D printing software aimed at RepRaps and the Ultimaker
Group:            Applications/Engineering

License:          GPLv2+
URL:              https://github.com/daid/Cura.git
Source0:          %{_curaName}-%{_version}.tar.gz

BuildRequires:    gcc-c++, libstdc++-static, glibc-static, cmake
Requires:         wxPython, curl, mesa-libGLU
Requires:         python2-setuptools >= 0.6.34
Requires:         python2-pyopengl >= 3.0.2
Requires:         python2-pyserial >= 2.6, pyserial >= 2.6
Requires:         python2-numpy >= 1.6.2, numpy >= 1.6.2
Requires:         python2-power >= 1.2


%description
%{_curaName} is a full software solution for 3D printing, aimed at RepRaps and
the Ultimaker.

It's free software payed for and maintained by Ultimaker.


%prep
%setup -q -n %{name}-%{version}


%build
cd CuraEngine
sh clean-build.sh production
cd ..

dstDir="%{_baseDir}/usr/share/cura"

rm    -frv "$dstDir"
mkdir -pv  "$dstDir"

cp -av -t  "$dstDir" \
  Cura \
  resources \
  plugins \
  CuraEngine/build/bin/CuraEngine \
  Power/power \
  scripts/linux/cura.py

echo "%{_version}" > "$dstDir/Cura/version"
cat > "$dstDir/Cura/versions" << EOF
# Git SHAs of software used to build %{_curaName}
Cura       : %{_gitCura}
CuraEngine : %{_gitCuraEngine}
Power      : %{_gitPower}
EOF


%install
mkdir -pv "%{buildroot}"
cp -av -t "%{buildroot}" "%{_baseDir}/usr"


%files
%defattr(-,root,root)
%{_bindir}/cura
%attr(644, root, root) %{_datarootdir}/applications/cura.desktop
%attr(755, root, root) %{_datarootdir}/cura/Cura/cura.py
%attr(755, root, root) %{_datarootdir}/cura/Cura/util/pymclevel/mce.py
%attr(755, root, root) %{_datarootdir}/cura/CuraEngine
%attr(755, root, root) %{_datarootdir}/cura/cura.py
%{_datarootdir}/cura


%changelog
* Wed Jan 14 2015 Ferry Huberts <ferry.huberts@pelagic.nl>
- Initial packaging, currently at version 15.01.RC7
