module R
#(parameter DATAWIDTH=4)
(   output reg [DATAWIDTH-1:0] Q,
    input  [DATAWIDTH-1:0] D,
    input CLK,
    input ce,
    input RESET
);
	always @(posedge CLK or posedge RESET)
	  begin
	  	if (RESET)
			Q = 0;	
	  	else if (ce)
			Q = D;
	  end

endmodule


