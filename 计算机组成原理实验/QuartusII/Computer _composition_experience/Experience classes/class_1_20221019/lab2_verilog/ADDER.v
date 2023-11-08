module ADDER 
#(parameter DATAWIDTH = 4)
(
input  [DATAWIDTH-1:0] A,B,
input  C0,
output [DATAWIDTH-1:0] F,
output [3:0] FLAG
);
wire [DATAWIDTH:0] result; 
wire S,Z,O,C;
assign result=A+B+C0;  
assign F =result[DATAWIDTH-1:0];
assign FLAG = {S,Z,O,C};

assign  S = F[DATAWIDTH-1];
assign  Z = (F==0) ? 1 : 0;  //~(|F);
assign  O = (~A[DATAWIDTH-1]) & ~B[DATAWIDTH-1] & F[DATAWIDTH-1] | (A[DATAWIDTH-1]) & B[DATAWIDTH-1] & ~F[DATAWIDTH-1] ;
assign  C = result[DATAWIDTH];

endmodule