`timescale 1ns / 1ps
module t_ff(
    input t,
    input clk,
    input rst,
    output reg q,
    output reg qbar
    );
    always @ (posedge clk)
    begin
        if(rst)
        q <= 0;
        
        else
        begin
            if(t)
            q <= ~q;
            
            else
            q <= q;
        end
    qbar = ~q;
    end
endmodule
