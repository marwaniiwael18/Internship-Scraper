{ pkgs }: {
  deps = [
    pkgs.python310Full
    pkgs.python310Packages.pip
    pkgs.python310Packages.flask
    pkgs.python310Packages.urllib3
    pkgs.python310Packages.python-dateutil
    pkgs.replitPackages.prybar-python310
    pkgs.curl
    pkgs.wget
    pkgs.git
  ];
  env = {
    PYTHONBIN = "${pkgs.python310Full}/bin/python3.10";
    LANG = "en_US.UTF-8";
    PYTHONIOENCODING = "utf-8";
    PYTHONHOME = pkgs.python310Full;
    PATH = "${pkgs.git}/bin:$PATH";
  };
}
