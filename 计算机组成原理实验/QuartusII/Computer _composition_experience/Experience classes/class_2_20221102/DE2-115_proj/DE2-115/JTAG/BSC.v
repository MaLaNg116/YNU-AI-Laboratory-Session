module BSC
#(  parameter DATAWIDTH=16)
(
    input  [DATAWIDTH-1:0] DataIn,
    output [DATAWIDTH-1:0] DataOut,
    input ScanIn,  ShiftDR, CaptureDR, UpdateDR, Mode, TCK,
    output ScanOut
);
	reg	[DATAWIDTH-1:0]	BSC_Capture_Register, BSC_Update_Register;

	always @ (posedge TCK) 
	begin
		if(CaptureDR)
			BSC_Capture_Register <= DataIn;
		else if (ShiftDR)
			BSC_Capture_Register <= {ScanIn, BSC_Capture_Register[DATAWIDTH-1:1]};
		else
			BSC_Capture_Register <= BSC_Capture_Register;
    end

	always @ (negedge TCK)
	begin 
		if(UpdateDR)
			BSC_Update_Register <= BSC_Capture_Register;
		else
			BSC_Update_Register <= BSC_Update_Register;
	end
	
	assign ScanOut = BSC_Capture_Register[0];
	assign DataOut = Mode ? BSC_Update_Register : DataIn;

endmodule
