#ifndef PANDORANUTRACK_CXX
#define PANDORANUTRACK_CXX

#include "PandoraNuTrack.h"
//#include "LArUtil/GeometryHelper.h"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
PandoraNuTrack::PandoraNuTrack( Int_t frun, Int_t fsubrun, Int_t fevent
                               ,Int_t ftrack_id
                               ,Float_t flength
                               ,Float_t ftheta, Float_t fphi
                               ,TVector3 fstart_pos, TVector3 fend_pos):
run(frun),
subrun(fsubrun),
event(fevent),
track_id(ftrack_id),
length(flength),
theta(ftheta),
phi(fphi),
start_pos(fstart_pos),
end_pos(fend_pos)
{

}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void PandoraNuTrack::Print() const{
    Printf("run/subrun/event : %d/%d/%d",run,subrun,event);
    Printf("track id: %d",track_id);
    Printf("length: %.1f cm, theta=%.2f rad, phi=%.2f rad",length,theta,phi);
    Printf("start position:");  start_pos.Print();
    Printf("end position:");    end_pos.Print();
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void PandoraNuTrack::SetStartEndPlane(Int_t plane ,
                                      Int_t start_wire, Int_t start_time ,
                                      Int_t end_wire, Int_t end_time ){
//        roi[plane] = box( start_wire , start_time , end_wire , end_time );
    switch (plane) {
        case 0:
            start_wire_u = start_wire;
            start_time_u = start_time;
            end_wire_u = end_wire;
            end_time_u = end_time;
            break;
        case 1:
            start_wire_v = start_wire;
            start_time_v = start_time;
            end_wire_v = end_wire;
            end_time_v = end_time;
            break;
        case 2:
            start_wire_y = start_wire;
            start_time_y = start_time;
            end_wire_y = end_wire;
            end_time_y = end_time;
            break;
            
        default:
            break;
    }
}





/*

 //....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void PandoraNuTrack::SetFlashInfo(Float_t fcftime, Float_t fcftimewidth, Float_t fcfzcenter, Float_t fcfzwidth, Float_t fcfycenter, Float_t fcfywidth, Float_t fcftotalpe, Float_t fcfdistance){
    cftime         = fcftime;
    cftimewidth    = fcftimewidth;
    cfzcenter      = fcfzcenter;
    cfzwidth       = fcfzwidth;
    cfycenter      = fcfycenter;
    cfywidth       = fcfywidth;
    cftotalpe      = fcftotalpe;
    cfdistance     = fcfdistance;
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void PandoraNuTrack::Set_dqdx (Float_t fstart_dqdx, Float_t fend_dqdx, Float_t ftot_dqdx, Int_t fnhits){
    Set_start_dqdx(fstart_dqdx);
    Set_end_dqdx(fend_dqdx);
    Set_tot_dqdx(ftot_dqdx);
    Set_nhits(fnhits);
    Set_avg_dqdx( (nhits>0) ? tot_dqdx/nhits : 0 );
    
    // fix start and end points by charge: If start charge is greater, flip track
    is_flipped = 0;
    if(fstart_dqdx > fend_dqdx) FlipTrack();
 
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void PandoraNuTrack::SetCalorimetry_Y ( std::vector <Float_t> fresidual_range_Y, std::vector <Float_t> fdEdx_Y, std::vector <Float_t> fEdep_Y, std::vector <Float_t> fdqdx_Y){
    residual_range_Y = fresidual_range_Y;
    NEdepYsteps = residual_range_Y.size();
    dEdx_Y = fdEdx_Y;
    Edep_Y = fEdep_Y;
    dqdx_Y = fdqdx_Y;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void PandoraNuTrack::FlipTrack(int debug){
    
    if(debug>0) Printf("flipping track %i",track_id);
    
    // flip start and end positions
    TVector3 tmp_pos = start_pos;
    start_pos   = end_pos;
    end_pos     = tmp_pos;
    
    // change angles
    theta       = 3.1416 - theta;
    phi         = (phi > 0 ? phi-3.1416 : phi+3.1416);
    
    Float_t tmp_dqdx = start_dqdx;
    start_dqdx  = end_dqdx;
    end_dqdx    = tmp_dqdx;
    
    //    for (int plane = 0 ; plane < 3 ; plane++ ){
    //
    //        Float_t tmp1 = dqdx_around_start[plane];
    //        dqdx_around_start[plane] = dqdx_around_end[plane];
    //        dqdx_around_end[plane] = tmp1;
    //
    //        Float_t tmp2 = dqdx_around_start_track_associated[plane];
    //        dqdx_around_start_track_associated[plane] = dqdx_around_end_track_associated[plane];
    //        dqdx_around_end_track_associated[plane] = tmp2;
    //    }
    //
    //    Float_t     tmp3 = dqdx_around_start_total;
    //    dqdx_around_start_total = dqdx_around_end_total;
    //    dqdx_around_end_total = tmp3;
    //
    //    Float_t     tmp4 = dqdx_around_start_track_associated_total;
    //    dqdx_around_start_track_associated_total = dqdx_around_end_track_associated_total;
    //    dqdx_around_end_track_associated_total = tmp4;

    is_flipped  = 1;
}






//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void PandoraNuTrack::Calorimetry(){
    
    // make some additional caloritric variables
    dqdx_diff     = end_dqdx - start_dqdx;
    dqdx_ratio    = end_dqdx/start_dqdx;
    
    // ask about the directionality of the track
    TopBottDir = (start_pos.y() > end_pos.y()) ? "Top->Bottom"              : "Bottom->Top"         ;
    ForBackDir = (start_pos.z() > end_pos.z()) ? "backward (against BNB)"   : "forward (along BNB)" ;
    LefRghtDir = (start_pos.x() > end_pos.x()) ? "Left -> Right"            : "Right -> Left"       ;
    
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void PandoraNuTrack::Straightness(){
    
    // get straightness (distance from start to end of track over reco'd length)
    distlenratio = ((end_pos-start_pos).Mag())/length;
    
    
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void PandoraNuTrack::SetMomentum(Float_t fmomrange, Float_t fmommsllhd ){

    // this is true only if this track was a muon
    momrange = fmomrange;
    mommsllhd = fmommsllhd;
    momeavgrangellhd = 0.5*(fmommsllhd+fmomrange);

}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
Float_t PandoraNuTrack::ClosestDistanceToOtherTrack( PandoraNuTrack other_track, std::string * fStartOrEnd ){
    Float_t MinDistanceToOtherTrack = 10000;
    std::string StartOrEnd = "None";
    Float_t DistanceStartStart = (start_pos - other_track.start_pos).Mag();
    if (MinDistanceToOtherTrack>DistanceStartStart)     {MinDistanceToOtherTrack = DistanceStartStart; StartOrEnd = "Start";}
    
    Float_t DistanceStartEnd = (start_pos - other_track.end_pos).Mag();
    if (MinDistanceToOtherTrack>DistanceStartEnd)       {MinDistanceToOtherTrack = DistanceStartEnd; StartOrEnd = "Start";}
    
    Float_t DistanceEndStart = (end_pos - other_track.start_pos).Mag();
    if (MinDistanceToOtherTrack>DistanceEndStart)       {MinDistanceToOtherTrack = DistanceEndStart; StartOrEnd = "End";}
    
    Float_t DistanceEndEnd = (end_pos - other_track.end_pos).Mag();
    if (MinDistanceToOtherTrack>DistanceEndEnd)         {MinDistanceToOtherTrack = DistanceEndEnd; StartOrEnd = "End";}
    
    
    if (fStartOrEnd!=nullptr) *fStartOrEnd = StartOrEnd;

    return MinDistanceToOtherTrack;
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
Float_t PandoraNuTrack::DistanceFromPoint( TVector3 position, std::string * fStartOrEnd  ){
    Float_t DistanceStart, DistanceEnd , distance = 1000;
    std::string StartOrEnd = "None";

    DistanceStart = ( start_pos - position).Mag();
    DistanceEnd = ( end_pos - position).Mag();
    if ( DistanceStart < DistanceEnd ){
        StartOrEnd = "Start";
        distance = DistanceStart;
    }
    else{
        StartOrEnd = "End";
        distance = DistanceEnd;
    }

    return distance;
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
bool PandoraNuTrack::IsWireTimeAlongTrack ( Int_t plane, Int_t wire , Float_t time ){
    // return true if the Plane/Wire/Time point is along the track
    // load GeometryHelper utility
    Float_t trajectory_time = trajectory_slope[plane] * wire + trajectory_intersect[plane];
    if ( fabs(time - trajectory_time) < 20. ) {
        return true;
    }
    return false;
}



//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
void PandoraNuTrack::Print(bool DoPrintPos, bool DoPrintPandoraNuFeatures, bool DoPrintPlanes){
    
    cout << "\033[31m"
    << "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^" << endl
    << "track " << track_id << endl
    << "-------------------"
    << "\033[0m" << endl;
    // SHOW3(run , subrun , event);
    if (DoPrintPos){
        SHOWTVector3(start_pos);
        SHOWTVector3(end_pos);
    }
    if (DoPrintPandoraNuFeatures){
        PrintPhys(length,"cm");
        PrintPhys(momrange,"MeV/c momentum from range");
        PrintPhys(mommsllhd,"MeV/c momentum from MCS LLHD");
        PrintPhys(momeavgrangellhd,"MeV/c momentum from MCS LLHD and range");
        SHOW(distlenratio);
        PrintPhys(theta,"radians");
        PrintPhys(phi,"radians");
        PrintPhys(start_dqdx,"ADC/cm");
        PrintPhys(end_dqdx,"ADC/cm");
        PrintPhys(tot_dqdx,"ADC/cm");
        PrintPhys(dQtotal,"ADC");
        SHOW3( cosmicscore, coscontscore , pidpida )
        SHOW2( cfdistance , cfdistance_start );
    }
    if (DoPrintPlanes){
        SHOW3( purtruth_U , purtruth_V   , purtruth_Y );
        for (int plane = 0 ; plane < 3; plane++) {
            PrintPhys( CalorimetryPDG[plane] , Form(" for plane %d",plane) );
            PrintBox(roi[plane]);
        }
    }
    if ( truth_Eng>0 && truth_P>0 ){
        cout << "MC information \n..................." << endl;
        SHOW ( mcevent_id );
        SHOW2 ( process_primary , MCpdgCode );
        PrintPhys (truth_P , "GeV/c");
        SHOW3(truth_Eng , truth_theta , truth_phi);
        PrintPhys(truth_length , "cm");
        SHOWTVector3(truth_start_pos);
        SHOWTVector3(truth_end_pos);
        SHOW2( truth_ccnc, IsGENIECC1p );
        SHOW( IsGENIECC_1p_200MeVc_0pi );
    }
    cout << "\033[31m"
    << "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"
    << "\033[0m" << endl;
}


*/
#endif