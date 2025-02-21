rule SVG_HTML 
{
  meta:
    description = "Yara attempt for SVG with HTML or JS"
	author = "Sherwyn B"
        date = "2025-1-22"

        strings:
		//svg header
        	$svg_header = "<svg"
		
		//html reference
		$href	= /<a\s+[^>]*href\s*=\s*["'][^"']*["'][^>]*>/i
		
		//js stuff
        	$script = /<script[\s\S]*?>[\s\S]*?<\/script>/i
		$alert  = /alert\([^\)]*\)/i
		
	        $iframe = /<iframe[\s\S]*?>[\s\S]*?<\/iframe>/i
	        $object = /<object[\s\S]*?>[\s\S]*?<\/object>/i
        
    condition:
        $svg_header at 0 and ($script or $iframe or $object or $href or $alert)
}
