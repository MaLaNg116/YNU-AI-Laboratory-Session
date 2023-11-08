module SEG7_LUT	(	oSEG,iDIG	);
input	[4:0]	iDIG;
output	[6:0]	oSEG;
reg		[6:0]	oSEG;

always @(iDIG)
begin
		case(iDIG)
		5'h1: oSEG = 7'b1111001;	// ---t----
		5'h2: oSEG = 7'b0100100; 	// |	  |
		5'h3: oSEG = 7'b0110000; 	// lt	 rt
		5'h4: oSEG = 7'b0011001; 	// |	  |
		5'h5: oSEG = 7'b0010010; 	// ---m----
		5'h6: oSEG = 7'b0000010; 	// |	  |
		5'h7: oSEG = 7'b1111000; 	// lb	 rb
		5'h8: oSEG = 7'b0000000; 	// |	  |
		5'h9: oSEG = 7'b0011000; 	// ---b----
		5'ha: oSEG = 7'b0001000;
		5'hb: oSEG = 7'b0000011;
		5'hc: oSEG = 7'b1000110;
		5'hd: oSEG = 7'b0100001;
		5'he: oSEG = 7'b0000110;
		5'hf: oSEG = 7'b0001110;
		5'h0: oSEG = 7'b1000000;
        default:oSEG = 7'b1111111;
		endcase
end

endmodule
