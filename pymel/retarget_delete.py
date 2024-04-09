import maya.cmds as cmds

cmds.select(cl = True)

#¿À¸¥ÂÊ´Ù¸®
cmds.select('DHIbody:ankle_bck_r')
cmds.select('DHIbody:ankle_fwd_r', add=True )
cmds.select('DHIbody:calf_twist_02_r', add=True )
cmds.select('DHIbody:calf_twist_01_r', add=True )
cmds.select('DHIbody:calf_correctiveRoot_r', add=True )
cmds.select('DHIbody:thigh_twist_01_r', add=True )
cmds.select('DHIbody:thigh_twist_02_r', add=True )
cmds.select('DHIbody:thigh_correctiveRoot_r', add=True )

#°¡½¿
cmds.select('DHIbody:clavicle_pec_r',add=True)
cmds.select('DHIbody:spine_04_latissimus_l',add=True)
cmds.select('DHIbody:clavicle_pec_l',add=True)
cmds.select('DHIbody:spine_04_latissimus_r',add=True)

#¼â°ñ
cmds.select('DHIbody:clavicle_out_r',add=True)
cmds.select('DHIbody:clavicle_scap_r',add=True)
cmds.select('DHIbody:clavicle_out_l',add=True)
cmds.select('DHIbody:clavicle_scap_l',add=True)

#¿ÞÂÊ´Ù¸®
cmds.select('DHIbody:ankle_bck_l',add=True)
cmds.select('DHIbody:ankle_fwd_l', add=True )
cmds.select('DHIbody:calf_twist_02_l', add=True )
cmds.select('DHIbody:calf_twist_01_l', add=True )
cmds.select('DHIbody:calf_correctiveRoot_l', add=True )
cmds.select('DHIbody:thigh_twist_01_l', add=True )
cmds.select('DHIbody:thigh_twist_02_l', add=True )
cmds.select('DHIbody:thigh_correctiveRoot_l', add=True )

#¿À¸¥ÂÊ¼Õ
cmds.select('DHIbody:upperarm_correctiveRoot_r',add=True)
cmds.select('DHIbody:upperarm_twist_01_r', add=True )
cmds.select('DHIbody:upperarm_twist_02_r', add=True )
cmds.select('DHIbody:lowerarm_correctiveRoot_r', add=True )
cmds.select('DHIbody:lowerarm_twist_01_r', add=True )
cmds.select('DHIbody:lowerarm_twist_02_r', add=True )

cmds.select('DHIbody:wrist_inner_r', add=True )
cmds.select('DHIbody:wrist_outer_r', add=True )

cmds.select('DHIbody:pinky_metacarpal_slide_r', add=True )

cmds.select('DHIbody:pinky_01_side_inn_r', add=True )
cmds.select('DHIbody:pinky_01_side_out_r', add=True )
cmds.select('DHIbody:pinky_01_half_r', add=True )
cmds.select('DHIbody:pinky_01_bulge_r', add=True )
cmds.select('DHIbody:pinky_01_palmMid_r', add=True )

cmds.select('DHIbody:pinky_02_dip_r', add=True )
cmds.select('DHIbody:pinky_02_half_r', add=True )
cmds.select('DHIbody:pinky_02_bulge_r', add=True )
cmds.select('DHIbody:pinky_02_side_out_r', add=True )
cmds.select('DHIbody:pinky_02_side_inn_r', add=True )

cmds.select('DHIbody:pinky_03_half_r', add=True )
cmds.select('DHIbody:pinky_03_bulge_r', add=True )


##
cmds.select('DHIbody:ring_metacarpal_slide_r', add=True )

cmds.select('DHIbody:ring_01_side_inn_r', add=True )
cmds.select('DHIbody:ring_01_side_out_r', add=True )
cmds.select('DHIbody:ring_01_half_r', add=True )
cmds.select('DHIbody:ring_01_bulge_r', add=True )
cmds.select('DHIbody:ring_01_palmMid_r', add=True )

cmds.select('DHIbody:ring_02_dip_r', add=True )
cmds.select('DHIbody:ring_02_half_r', add=True )
cmds.select('DHIbody:ring_02_bulge_r', add=True )
cmds.select('DHIbody:ring_02_side_out_r', add=True )
cmds.select('DHIbody:ring_02_side_inn_r', add=True )

cmds.select('DHIbody:ring_03_half_r', add=True )
cmds.select('DHIbody:ring_03_bulge_r', add=True )

##
cmds.select('DHIbody:middle_metacarpal_slide_r', add=True )

cmds.select('DHIbody:middle_01_side_inn_r', add=True )
cmds.select('DHIbody:middle_01_side_out_r', add=True )
cmds.select('DHIbody:middle_01_half_r', add=True )
cmds.select('DHIbody:middle_01_bulge_r', add=True )
cmds.select('DHIbody:middle_01_palmMid_r', add=True )

cmds.select('DHIbody:middle_02_dip_r', add=True )
cmds.select('DHIbody:middle_02_half_r', add=True )
cmds.select('DHIbody:middle_02_bulge_r', add=True )
cmds.select('DHIbody:middle_02_side_out_r', add=True )
cmds.select('DHIbody:middle_02_side_inn_r', add=True )

cmds.select('DHIbody:middle_03_half_r', add=True )
cmds.select('DHIbody:middle_03_bulge_r', add=True )

##
cmds.select('DHIbody:index_metacarpal_slide_r', add=True )

cmds.select('DHIbody:index_01_side_inn_r', add=True )
cmds.select('DHIbody:index_01_side_out_r', add=True )
cmds.select('DHIbody:index_01_half_r', add=True )
cmds.select('DHIbody:index_01_bulge_r', add=True )
cmds.select('DHIbody:index_01_palmMid_r', add=True )

cmds.select('DHIbody:index_02_dip_r', add=True )
cmds.select('DHIbody:index_02_half_r', add=True )
cmds.select('DHIbody:index_02_bulge_r', add=True )
cmds.select('DHIbody:index_02_side_out_r', add=True )
cmds.select('DHIbody:index_02_side_inn_r', add=True )

cmds.select('DHIbody:index_03_half_r', add=True )
cmds.select('DHIbody:index_03_bulge_r', add=True )


##
cmds.select('DHIbody:thumb_01_side_out_r', add=True )
cmds.select('DHIbody:thumb_01_side_inn_r', add=True )

cmds.select('DHIbody:thumb_02_half_r', add=True )
cmds.select('DHIbody:thumb_02_side_out_r', add=True )
cmds.select('DHIbody:thumb_02_side_inn_r', add=True )
cmds.select('DHIbody:thumb_02_bulge_r', add=True )

##
cmds.select('DHIbody:thumb_03_half_r', add=True )
cmds.select('DHIbody:thumb_03_side_out_r', add=True )
cmds.select('DHIbody:thumb_03_side_inn_r', add=True )
cmds.select('DHIbody:thumb_03_bulge_r', add=True )


#¿ÞÂÊ¼Õ
cmds.select('DHIbody:upperarm_correctiveRoot_l',add=True)
cmds.select('DHIbody:upperarm_twist_01_l', add=True )
cmds.select('DHIbody:upperarm_twist_02_l', add=True )
cmds.select('DHIbody:lowerarm_correctiveRoot_l', add=True )
cmds.select('DHIbody:lowerarm_twist_01_l', add=True )
cmds.select('DHIbody:lowerarm_twist_02_l', add=True )

cmds.select('DHIbody:wrist_inner_l', add=True )
cmds.select('DHIbody:wrist_outer_l', add=True )

cmds.select('DHIbody:pinky_metacarpal_slide_l', add=True )

cmds.select('DHIbody:pinky_01_side_inn_l', add=True )
cmds.select('DHIbody:pinky_01_side_out_l', add=True )
cmds.select('DHIbody:pinky_01_half_l', add=True )
cmds.select('DHIbody:pinky_01_bulge_l', add=True )
cmds.select('DHIbody:pinky_01_palmMid_l', add=True )

cmds.select('DHIbody:pinky_02_dip_l', add=True )
cmds.select('DHIbody:pinky_02_half_l', add=True )
cmds.select('DHIbody:pinky_02_bulge_l', add=True )
cmds.select('DHIbody:pinky_02_side_out_l', add=True )
cmds.select('DHIbody:pinky_02_side_inn_l', add=True )

cmds.select('DHIbody:pinky_03_half_l', add=True )
cmds.select('DHIbody:pinky_03_bulge_l', add=True )


##
cmds.select('DHIbody:ring_metacarpal_slide_l', add=True )

cmds.select('DHIbody:ring_01_side_inn_l', add=True )
cmds.select('DHIbody:ring_01_side_out_l', add=True )
cmds.select('DHIbody:ring_01_half_l', add=True )
cmds.select('DHIbody:ring_01_bulge_l', add=True )
cmds.select('DHIbody:ring_01_palmMid_l', add=True )

cmds.select('DHIbody:ring_02_dip_l', add=True )
cmds.select('DHIbody:ring_02_half_l', add=True )
cmds.select('DHIbody:ring_02_bulge_l', add=True )
cmds.select('DHIbody:ring_02_side_out_l', add=True )
cmds.select('DHIbody:ring_02_side_inn_l', add=True )

cmds.select('DHIbody:ring_03_half_l', add=True )
cmds.select('DHIbody:ring_03_bulge_l', add=True )

##
cmds.select('DHIbody:middle_metacarpal_slide_l', add=True )

cmds.select('DHIbody:middle_01_side_inn_l', add=True )
cmds.select('DHIbody:middle_01_side_out_l', add=True )
cmds.select('DHIbody:middle_01_half_l', add=True )
cmds.select('DHIbody:middle_01_bulge_l', add=True )
cmds.select('DHIbody:middle_01_palmMid_l', add=True )

cmds.select('DHIbody:middle_02_dip_l', add=True )
cmds.select('DHIbody:middle_02_half_l', add=True )
cmds.select('DHIbody:middle_02_bulge_l', add=True )
cmds.select('DHIbody:middle_02_side_out_l', add=True )
cmds.select('DHIbody:middle_02_side_inn_l', add=True )

cmds.select('DHIbody:middle_03_half_l', add=True )
cmds.select('DHIbody:middle_03_bulge_l', add=True )

##
cmds.select('DHIbody:index_metacarpal_slide_l', add=True )

cmds.select('DHIbody:index_01_side_inn_l', add=True )
cmds.select('DHIbody:index_01_side_out_l', add=True )
cmds.select('DHIbody:index_01_half_l', add=True )
cmds.select('DHIbody:index_01_bulge_l', add=True )
cmds.select('DHIbody:index_01_palmMid_l', add=True )

cmds.select('DHIbody:index_02_dip_l', add=True )
cmds.select('DHIbody:index_02_half_l', add=True )
cmds.select('DHIbody:index_02_bulge_l', add=True )
cmds.select('DHIbody:index_02_side_out_l', add=True )
cmds.select('DHIbody:index_02_side_inn_l', add=True )

cmds.select('DHIbody:index_03_half_l', add=True )
cmds.select('DHIbody:index_03_bulge_l', add=True )


##
cmds.select('DHIbody:thumb_01_side_out_l', add=True )
cmds.select('DHIbody:thumb_01_side_inn_l', add=True )

cmds.select('DHIbody:thumb_02_half_l', add=True )
cmds.select('DHIbody:thumb_02_side_out_l', add=True )
cmds.select('DHIbody:thumb_02_side_inn_l', add=True )
cmds.select('DHIbody:thumb_02_bulge_l', add=True )

##
cmds.select('DHIbody:thumb_03_half_l', add=True )
cmds.select('DHIbody:thumb_03_side_out_l', add=True )
cmds.select('DHIbody:thumb_03_side_inn_l', add=True )
cmds.select('DHIbody:thumb_03_bulge_l', add=True )



