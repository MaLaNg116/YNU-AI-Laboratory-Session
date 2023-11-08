module uAG
(
    output reg [5:0] uAGOut,
    input [9:6] IR,
	input [5:0] NA,
	input [1:0] BM
);   
	always @ *
	  begin
	  	case (BM)
		  2'b00:	uAGOut = NA;             
		  2'b01:  uAGOut = {NA[5:1], | IR[9:6] };
          2'b10:	uAGOut = {2'b01, IR[9:6]};  
          default:uAGOut = {6'bxxxxxx};
		endcase
	  end
endmodule
