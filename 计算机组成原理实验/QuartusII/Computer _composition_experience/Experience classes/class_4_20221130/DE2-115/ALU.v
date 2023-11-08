module ALU
#(parameter DATAWIDTH=4)
(
   input [DATAWIDTH-1:0]dst,src,
   input [3:0] ALU_OP,
   input CF,			//来自PSW的CF位
   output [DATAWIDTH-1:0]F,
   output [3:0] FLAG   //运算结果的标志位输出
);

wire ADD,ADDC,SUB,SUBB,AND,OR,NOT,XOR,INC,DEC,NOP;
wire [DATAWIDTH-1:0] A = dst;
wire [DATAWIDTH-1:0] B; 
wire C0;
wire M3,M2,M1,M0;

//运算控制信号译码
assign{DEC,INC,XOR,NOT,OR,AND,SUBB,SUB,ADDC,ADD, NOP} = 2**(ALU_OP);

assign M0 = ADD|ADDC|SUB|SUBB;
assign M1 = SUB|SUBB|DEC;
assign M2 = SUB|INC;
assign M3 = ADDC|SUBB;
assign B = {DATAWIDTH{M1}} ^ (src & {DATAWIDTH{M0}});
assign C0 = (CF & M3) | (M2);

reg [DATAWIDTH:0] result;
always @(*)
begin
   case ({AND, OR, NOT, XOR})
      4'b1000: result = {1'b0, (dst & src)};
      4'b0100: result = {1'b0, (dst | src)};
      4'b0010: result = {1'b0, (~dst)};
      4'b0001: result = {1'b0, (dst ^ src)};
      default: result = A + B + C0;
   endcase
end
	 
wire S,Z,O,C;
assign F  = result[DATAWIDTH-1:0];
assign FLAG = {S,Z,O,C};
assign S = F[DATAWIDTH-1];
assign Z = ~(|F);
assign O = (~A[DATAWIDTH-1]) & ~B[DATAWIDTH-1] & F[DATAWIDTH-1] | (A[DATAWIDTH-1]) & B[DATAWIDTH-1] & ~F[DATAWIDTH-1] ;
assign C = result[DATAWIDTH];
  
endmodule
