`timescale 1ns/1ps

module dff (c,d,res,q);
   input wire c, d, res;
   output reg q;

   always @(posedge c or negedge res)
     begin
       if (!res) q <= 1'b0;
       else q <= d;
     end

endmodule
