// Поиск последовательности 10010

module seqdet_10010 (nrst, clk, ain, zout);

input          nrst,clk;
input          ain;
output         zout;
reg            zout;

reg    [3:0]   nextstate,currentstate;
reg            temp_z;


parameter s0  = 4'b0000,
          s1  = 4'b0001,
          s2  = 4'b0010,
          s3  = 4'b0100,
          s4  = 4'b1000;


always @ (posedge clk or negedge nrst)
 if (!nrst)
    currentstate <= s0;
 else
    currentstate <= nextstate;


always @ (currentstate or ain)
    begin
      case (currentstate)
        s0:      nextstate = (ain==1) ? s1 : s0;
        s1:      nextstate = (ain==0) ? s2 : s1;
        s2:      nextstate = (ain==0) ? s3 : s1;
        s3:      nextstate = (ain==1) ? s4 : s0;
        s4:      nextstate = (ain==0) ? s2 : s1;
        default: nextstate = 4'bxxxx;
      endcase
   end


always@(nrst or currentstate or ain)
   if(!nrst)
     temp_z = 0;
   else
     case(currentstate)
        s0: temp_z = 1'b0;
        s1: temp_z = 1'b0;
        s2: temp_z = 1'b0;
        s3: temp_z = 1'b0;
        s4: temp_z = (ain == 0) ? 1'b1 : 1'b0;
        default:temp_z = 1'b0;
     endcase

always@(posedge clk or negedge nrst)
    if(!nrst)
       zout <= 0;
    else
       begin
         if((temp_z == 1'b1)&&(nextstate== s2))
           zout <= 1;
         else
           zout <= 0;
       end

endmodule
