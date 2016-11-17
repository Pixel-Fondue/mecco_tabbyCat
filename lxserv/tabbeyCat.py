#python

import lx, lxu

NAME_CMD_tabKey = "tabbyCat.tab"

def selMode(target=None):
  modes = 'vertex;edge;polygon;item;pivot;center;ptag'
  if not target:
    for mode in modes.split(';'):
        if lx.eval('select.typeFrom %s;%s ?' % (mode, modes)):
            return mode
  else:
    lx.eval('select.typeFrom %s;%s' % (target, modes))


class CMD_tabbyCat_tabKey(lxu.command.BasicCommand):

    def __init__(self):
        lxu.command.BasicCommand.__init__(self)

    def cmd_Flags (self):
        #make the command undoable
        return lx.symbol.fCMD_MODEL | lx.symbol.fCMD_UNDO

    def basic_Execute(self, msg, flags):
        originalMode = selMode()

        selMode('polygon')
        originalPolySel = lx.eval('query layerservice polys ? selected')
        lx.eval('select.editSet originalPolySel set')
        selMode(originalMode)

        if originalMode == 'vertex':
          originalSel = lx.eval('query layerservice verts ? selected')
          lx.eval('select.editSet originalSel set')

          selMode('polygon')
          originalPolySel = lx.eval('query layerservice polys ? selected')
          lx.eval('select.editSet originalPolySel set')

          selMode(originalMode)
          if originalSel:
            lx.eval('select.connect')
          else:
            lx.eval('select.all')
          lx.eval('select.convert polygon')

        elif originalMode == 'edge':
          originalSel = lx.eval('query layerservice edges ? selected')
          lx.eval('select.editSet originalSel set')

          selMode('polygon')
          originalPolySel = lx.eval('query layerservice polys ? selected')
          lx.eval('select.editSet originalPolySel set')

          selMode(originalMode)
          if originalSel:
            lx.eval('select.connect')
          else:
            lx.eval('select.all')
          lx.eval('select.convert polygon')

        elif originalMode == 'polygon':
          originalSel = lx.eval('query layerservice polys ? selected')
          lx.eval('select.editSet originalSel set')

          if originalSel:
            lx.eval('select.connect')
          else:
            lx.eval('select.all')

        elif originalMode == 'ptag':
          selMode('polygon')
          originalPolySel = lx.eval('query layerservice polys ? selected')
          lx.eval('select.editSet originalPolySel set')

          selMode('ptag')
          lx.eval('select.convert polygon')
          if lx.eval('query layerservice polys ? selected'):
            lx.eval('select.connect')
          else:
            lx.eval('select.all')

        elif originalMode in ['item','pivot','center']:
          selMode('polygon')
          lx.eval('select.all')

        selMode('polygon')
        lx.eval('select.editSet extendedSel set')

        lx.eval('select.polygon remove type face 0')
        if lx.eval('query layerservice polys ? selected'):
          target = "face"
        else:
          target = "psubdiv"

        lx.eval('select.useSet extendedSel replace')
        lx.eval('poly.convert %s face toggle:false' % target)
        lx.eval('!poly.align')
        lx.eval('select.drop polygon')



        if originalPolySel:
          lx.eval('select.useSet originalPolySel replace')
        lx.eval('select.deleteSet originalPolySel')
        lx.eval('select.deleteSet extendedSel')

        selMode(originalMode)

        if originalMode in ['vertex','edge','polygon']:
          lx.eval('select.drop %s' % originalMode)
          if originalSel:
            lx.eval('select.useSet originalSel replace')

          lx.eval('select.deleteSet originalSel')



lx.bless(CMD_tabbyCat_tabKey, NAME_CMD_tabKey)
