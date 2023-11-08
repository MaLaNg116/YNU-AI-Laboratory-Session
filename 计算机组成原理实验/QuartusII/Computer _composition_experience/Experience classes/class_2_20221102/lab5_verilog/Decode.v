// 2 to 4 Decod
module Decode (
    input Enable,
    input [1:0] DIN,
    output [3:0] DOUT
);

    reg [3:0] D_OUT;
    always @*
    begin
       case (DIN)
         2'b00 : D_OUT <= 4'b0001;
         2'b01 : D_OUT <= 4'b0010;
         2'b10 : D_OUT <= 4'b0100;
         2'b11 : D_OUT <= 4'b1000;
         default : D_OUT <= 4'b0000;
       endcase 
    end
    assign DOUT = Enable ? D_OUT : 4'b0000;
    
endmodule
