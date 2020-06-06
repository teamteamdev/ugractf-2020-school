{
  binPackages = pkgs: with pkgs; [
    coreutils
    bash
    nodejs
  ];

  pythonPackages = self: with self; [
    scapy
    gunicorn
    aiohttp
    aiohttp-jinja2
    pillow
    python-barcode
  ];
}
