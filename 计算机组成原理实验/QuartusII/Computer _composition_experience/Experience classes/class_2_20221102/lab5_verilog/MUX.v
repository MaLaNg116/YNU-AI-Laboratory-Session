// 4 to 1 multiplexer design with case construct

module MUX
#(parameter WIDTH = 4)
(
    input [WIDTH-1:0] A,
    input [WIDTH-1:0] B,
    input [WIDTH-1:0] C,
    input [WIDTH-1:0] D,
    input [1:0] SEL,
    output reg [WIDTH-1:0] MUX_OUT
);
    always @(SEL or A or B or C or D)
      begin
        case (SEL)
          2'b00 : MUX_OUT = A;
          2'b01 : MUX_OUT = B;
          2'b10 : MUX_OUT = C;
          2'b11 : MUX_OUT = D;
          default : MUX_OUT = 0;
        endcase
      end
endmodule
