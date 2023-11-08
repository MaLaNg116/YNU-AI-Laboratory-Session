module GRS
#(parameter DATAWIDTH=4, parameter INDEXWIDTH=2)
(
    input   [DATAWIDTH-1:0] D,
    output  [DATAWIDTH-1:0] Q,
	input   ce,
	input   CLK,
	input   [INDEXWIDTH-1:0] INDEX
);
    localparam DEPTH = 1<<INDEXWIDTH;
    reg [DATAWIDTH-1:0] regSet [0:DEPTH-1]; 
	always @(posedge CLK) 
    begin
        if(ce)
            regSet[INDEX] = D;
    end
	assign  Q = regSet[INDEX];

endmodule

