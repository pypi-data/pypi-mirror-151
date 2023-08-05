#####################################################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#	- This file is a part of the VocalTractLab Python module PyVTL, see https://github.com/paul-krug/VocalTractLab
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#
#	- Copyright (C) 2021, Paul Konstantin Krug, Dresden, Germany
#	- https://github.com/paul-krug/VocalTractLab
#	- Author: Paul Konstantin Krug, TU Dresden
#
#	- License info:
#
#		This program is free software: you can redistribute it and/or modify
#		it under the terms of the GNU General Public License as published by
#		the Free Software Foundation, either version 3 of the License, or
#		(at your option) any later version.
#		
#		This program is distributed in the hope that it will be useful,
#		but WITHOUT ANY WARRANTY; without even the implied warranty of
#		MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#		GNU General Public License for more details.
#		
#		You should have received a copy of the GNU General Public License
#		along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#####################################################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------------------------------------------------------------------------------------------------------------#
#####################################################################################################################################################
#---------------------------------------------------------------------------------------------------------------------------------------------------#
'''Load essential packages:'''
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#import VocalTractLab.VocalTractLabApi as vtl
# VocalTractLab.plotting_tools as PT
from VocalTractLab.plotting_tools import finalize_plot
from VocalTractLab.plotting_tools import get_plot
from VocalTractLab.plotting_tools import get_plot_limits
import numpy as np
import matplotlib.pyplot as plt
#---------------------------------------------------------------------------------------------------------------------------------------------------#
#####################################################################################################################################################





#####################################################################################################################################################
class Tube_State():
	def __init__( self, 
		          tube_length,
		          tube_area,
		          tube_articulator,
		          incisor_position,
		          tongue_tip_side_elevation,
		          velum_opening,
		          ):
		self.tube_length = tube_length
		self.tube_area = tube_area
		self.tube_articulator = tube_articulator
		self.incisor_position = incisor_position
		self.tongue_tip_side_elevation = tongue_tip_side_elevation
		self.velum_opening = velum_opening
		self.constriction = self.get_constriction()
		return
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def get_constriction( self, return_str = False ):
		open_limit = 0.3  # 0.3 cm^2 for open tracts
		tight_limit = 0.001 # above 0.001 tight, below or equal closed
		constriction_strings = [ 'open', 'tight', 'closed' ]
		min_area = np.min( self.tube_area )
		constriction = None
		if min_area >= open_limit:
			constriction = 0
		elif min_area > tight_limit:
			constriction = 1
		elif min_area <= tight_limit:
			constriction = 2
		if not return_str:
			return constriction
		else:
			return constriction_strings[ constriction ]
#---------------------------------------------------------------------------------------------------------------------------------------------------#
	def plot( self, 
	          axs = None, 
			  **kwargs,
	          ):
		figure, axs = get_plot( n_rows = 1, axs = axs )
		tube_x = [ self.tube_length[ 0 ] ]
		for length in self.tube_length[ 1: ]:
			tube_x.append( tube_x[ -1 ] + length )
		x = np.arange( 0, np.sum( self.tube_length ), 0.01 )
		y = []
		tmp_length = 0
		for index, _ in enumerate( self.tube_length ): 
			for val in x:
				if val >= tmp_length:
					if val <= tube_x[ index ]:
						y.append( self.tube_area[ index ] )
					else:
						tmp_length = tube_x[ index ]
						break
		axs[0].set( xlabel = 'Tube Length [cm]', ylabel = r'Cross-sectional Area [cm$^2$]' )
		#y = [ val for val in x  ]
		#x = [ self.tube_length[ 0 ] ]
		#for length in self.tube_length[ 1: ]:
		#	x.append( x[ -1 ] + length )
		axs[0].plot( x, y )
		finalize_plot( figure, axs, **kwargs )
		#ax.set( xlabel = 'Tube Length [cm]', ylabel = r'Cross-sectional Area [cm$^2$]' )
		return axs
#---------------------------------------------------------------------------------------------------------------------------------------------------#