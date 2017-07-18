/**
 * \file hit.h
 *
 * \ingroup GBDTprotonsPackage
 *
 * \brief Class def header for a class Hit
 *
 * @author erezcohen
 */

/** \addtogroup GBDTprotonsPackage
 
 @{*/
#ifndef hit_H
#define hit_H

#include "Rtypes.h"



class hit{
    
public:
    
    /// Default constructor
    hit () = default;
    hit (Int_t fplane, Int_t fwire, Int_t fid, Float_t fpeakT, Float_t fcharge);
    
    
    void    Print () const;
    
    /// SETters
    void               SetTrackKey (Int_t _key)      {hit_trkKey = _key;};
    
    
    // GETters
    Int_t              GetTrackKey ()   const {return hit_trkKey;};
    Int_t                 GetPlane ()   const {return hit_plane;};
    Int_t                  GetWire ()   const {return hit_wire;};
    Int_t                    GetID ()   const {return hit_id;};
    Float_t              GetCharge ()   const {return hit_charge;};
    Float_t               GetPeakT ()   const {return hit_peakT;};

    
    
//    inline bool operator==(const hit & h) {
//        return std::tie( hit_plane, hit_wire , hit_peakT , hit_id) == std::tie(h.hit_plane , h.hit_wire, h.hit_peakT , h.hit_id);
//    }
//    inline bool InBox(box b){
//        return (b.start_wire < hit_wire && hit_wire < b.end_wire && b.start_time < hit_peakT && hit_peakT < b.end_time);
//    }
    
    
    
    
    
    
    
    
private:
    
    // Int_t features
    Int_t       hit_plane=0,    hit_wire=0, hit_id=0,  hit_trkKey=-9999;
    
    
    
    // Float_t features
    Float_t     hit_peakT=0,    hit_charge=0;
    
    
};
#endif
/** @} */ // end of doxygen group

