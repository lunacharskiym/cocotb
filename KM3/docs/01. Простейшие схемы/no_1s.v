// Подсчёт числа единиц в 16-ти битном слове
module no_1s (i_a, clk, reset, no_ones);

input clk, reset                             ;
input       [15:0] i_a                       ;// входное слово 16 бит
output reg  [ 3:0] no_ones                   ;// число единиц во входном слове
integer i = 1'b0 ;

always @ (posedge clk)
   begin
      if (reset)
         no_ones <= 4'b0                     ;//по уровню reset счётчик сбрасывается в 0
      else
         begin
            if (i < 16)
               no_ones <= no_ones + i_a[i]   ;
         end
      i <= i + 1                             ;
   end

endmodule
