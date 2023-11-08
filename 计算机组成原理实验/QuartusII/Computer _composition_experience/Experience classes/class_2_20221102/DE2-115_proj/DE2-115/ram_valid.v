module ram_valid
#(parameter ADDRWIDTH=3)
(
	input   RESET,
	input   WR,
	input   [ADDRWIDTH-1:0] ADDR,
    output  VALID,
    output  [2**ADDRWIDTH-1:0] V_LED
);
    localparam DEPTH = 1<<ADDRWIDTH;
    wire mem[0:DEPTH-1];
    wire [DEPTH-1:0]wr;
    
    assign wr = WR ? 2**ADDR : 0;
    
    generate
        genvar i;
        for(i=0; i<DEPTH; i=i+1)
        begin: r
            R v(.D(1'b1), .Q(mem[i]), .CLK(wr[i]), .ce(1'b1), .RESET(RESET));
            assign  V_LED[i] = mem[i];
       end
    endgenerate

	assign  VALID = mem[ADDR];

endmodule

