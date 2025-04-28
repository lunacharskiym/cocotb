module seqdet_10010_Moore ( nrst, clk, ain, zout);

input        nrst,clk;
input        ain;
output       zout;
reg          zout;

reg    [4:0] nextstate,currentstate;


parameter s0  = 5'b00000,
          s1  = 5'b00001,
          s2  = 5'b00010,
          s3  = 5'b00100,
          s4  = 5'b01000,
          s5  = 5'b10000;


always @ (posedge clk or negedge nrst)
 if (!nrst)
    currentstate <= s0;
 else
    currentstate <= nextstate;


always @ (currentstate or ain)
    begin
      case (currentstate)
        s0:    nextstate = (ain==1)?s1:s0;
        s1:    nextstate = (ain==0)?s2:s1;
        s2:    nextstate = (ain==0)?s3:s1;
        s3:    nextstate = (ain==1)?s4:s0;
        s4:    nextstate = (ain==0)?s5:s1;
        s5:    nextstate = (ain==0)?s3:s1;
        default:   nextstate = 5'bxxxxx;
      endcase
   end


always @ (nrst or currentstate)
    begin
        if(!nrst)
            zout = 0;
        else
            case(currentstate)
                s0:    zout = 0;
                s1:    zout = 0;
                s2:    zout = 0;
                s3:    zout = 0;
                s4:    zout = 0;
                s5:    zout = 1;
                default:    zout = 0;
        endcase
    end

endmodule
