rule Purelogs_Stealer
{
    meta:
        description = "Purelogs Stealer variant test120922139213"
        author = "Sherwyn B"
        date = "2025-08-16"
        sha256 = "7505e02f9e72ce781892c01ac7638a8fac011f39c020cda61e2eada9eee1c31d"

    strings:
        $MZ        = { 4D 5A }
        $reg_full  = "HKEY_CURRENT_USER\\Software\\IqswyHgVpagFHxu" nocase
        $reg_short = "IqswyHgVpagFHxu"
        $ip_full   = "65.21.119.48"
        $port      = "6561"
        $mutex     = "FQBnanyetMxSRRO"
        $variant   = "test120922139213"

    condition:
        ($MZ and all of ($reg_full, $ip_full, $port))
        or
        any of ($reg_short, $mutex, $variant)
}
