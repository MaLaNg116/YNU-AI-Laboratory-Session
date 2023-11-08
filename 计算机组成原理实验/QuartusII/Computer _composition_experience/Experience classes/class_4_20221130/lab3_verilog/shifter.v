module SHIFTER
#(parameter DATAWIDTH = 4)  
(
    output [DATAWIDTH-1:0] Q,
    input  [DATAWIDTH-1:0] D,
    input  CLK,
    input  [1:0]ST_OP,
    input  RESET
);
reg [DATAWIDTH-1:0] data;

always @(posedge CLK or posedge RESET)    
begin
    if (RESET)
        data = 0;
    else
      case (ST_OP)
        2'b11:  data = D ;
        2'b10:  data = {D[DATAWIDTH-2:0], 1'b0};
        2'b01:  data = {1'b0, D[DATAWIDTH-1:1]};
        default:data = data;
      endcase
end

assign Q = data;

endmodule
