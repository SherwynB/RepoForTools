rule FormBook2025 {
    // This is the code snippet from the assembly loading the second stage.
    // if (remaining >= 3)
			// {
				// int num2 = ((int)pixel.R << 16) | ((int)pixel.G << 8) | (int)pixel.B;
				// bytes.AddRange(new byte[]
				// {
					// (byte)((num2 >> 16) & 255),
					// (byte)((num2 >> 8) & 255),
					// (byte)(num2 & 255)
				// });
				// if (num * num2 < 0)
				// {
					// text += "error";
					// return;
				// }
			// }
			// else if (remaining > 0)
			// {
				// Form1.Jupiter(bytes, Form1.Starlight(pixel), remaining);
				// foreach (int num3 in new List<int> { 1, 2, 3 })
				// {
					// num += num3;
				// }
			// }
		// }
  // ====== 
  // private static void Cupcake(Bitmap src, List<byte> bytes, int x, int length)
		// {
			// int num = 0;
			// while (num < src.Height && bytes.Count < length)
			// {
				// Color pixel = src.GetPixel(x, num);
				// int num2 = length - bytes.Count;
				// Form1.Pizza(bytes, pixel, num2);
				// num++;
			// }
		// }

    meta:
        description = "Second Stage Loading of Formbook 'Steganoraphy 2025' Sample"
	author = "Sherwyn B"
        date = "2025-1-21"
        sha256 = "320DAF03F7F2B9E697955EBC5C479C51FA3FB32CAF789187C54B52749550305A"

    strings:
        $MZ = { 4D 5A }
        $pizza_opcode1 = {   0F01 288D00000A 1F10 62 0F01 288E00000A 1E 62 60 0F01 288F00000A 60 0D 02 19 8D4A000001 25 16 09 1F10 63 20FF000000 5F D2 9C 25 17 09 1E 63 20FF000000 5F D2 9C 25 18 09 20FF000000 5F D2 9C 6F9200000A 06 09 5A 16 2F68 07 723D0A0070 282100000A 0B 2A 04   }
		$pizza_opcode2 = {  04 16 3157 02 03 283A000006 04 283F000006 739300000A 25 17 6F9400000A 25 18 6F9400000A 25 19 6F9400000A 6F9500000A 1304 2B0E 1204 289600000A 1305 06 1105 58 0A 1204 289700000A 2DE9 DE0E 1204 FE160800001B 6F5600000A DC 2A }
		$cupcake_opcode1 = { 16 0A 2B1E 02 04 06 6F9800000A 0B 05 03 6F9900000A 59 0C 03 07 08 2840000006 06 17 58 0A 06 02 6F7600000A 2F09 03 6F9900000A 05 32D0 2A }
    condition:
        ($MZ) and (all of ($pizza_opcode*) or $cupcake_opcode1)
}