{
  binPackages = pkgs: with pkgs; [
    coreutils
    bash
  ];

  pythonPackages = self: with self; [
    scapy
    gunicorn
    aiohttp
    aiohttp-jinja2
  ];
}
