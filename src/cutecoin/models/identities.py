'''
Created on 5 févr. 2014

@author: inso
'''

from ucoinpy.api import bma
from ..core.person import Person
from ..tools.exceptions import NoPeerAvailable, MembershipNotFoundError
from PyQt5.QtCore import QAbstractTableModel, QSortFilterProxyModel, Qt, \
                        QDateTime, QModelIndex, QLocale
from PyQt5.QtGui import QColor
import logging


class IdentitiesFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.community = None

    def setSourceModel(self, sourceModel):
        self.community = sourceModel.community
        super().setSourceModel(sourceModel)

    def lessThan(self, left, right):
        """
        Sort table by given column number.
        """
        source_model = self.sourceModel()
        left_data = source_model.data(left, Qt.DisplayRole)
        right_data = source_model.data(right, Qt.DisplayRole)
        left_data = 0 if left_data is None else left_data
        right_data = 0 if right_data is None else right_data
        return (left_data < right_data)

    def data(self, index, role):
        source_index = self.mapToSource(index)
        source_data = self.sourceModel().data(source_index, role)
        expiration_col = self.sourceModel().columns_ids.index('expiration')
        expiration_index = self.sourceModel().index(source_index.row(), expiration_col)
        expiration_data = self.sourceModel().data(expiration_index, Qt.DisplayRole)
        current_time = QDateTime().currentDateTime().toMSecsSinceEpoch()
        sig_validity = self.community.parameters['sigValidity']
        warning_expiration_time = int(sig_validity / 3)
        #logging.debug("{0} > {1}".format(current_time, expiration_data))
        if expiration_data is not None:
            will_expire_soon = (current_time > expiration_data*1000 - warning_expiration_time*1000)
        if role == Qt.DisplayRole:
            if source_index.column() == self.sourceModel().columns_ids.index('renewed') \
                    or source_index.column() == self.sourceModel().columns_ids.index('expiration'):
                if source_data is not None:
                    return QLocale.toString(
                        QLocale(),
                        QDateTime.fromTime_t(source_data).date(),
                        QLocale.dateFormat(QLocale(), QLocale.ShortFormat)
                    )
                else:
                    return ""
            if source_index.column() == self.sourceModel().columns_ids.index('pubkey'):
                return "pub:{0}".format(source_data[:5])

        if role == Qt.ForegroundRole:
            if expiration_data:
                if will_expire_soon:
                    return QColor(Qt.red)
            else:
                return QColor(Qt.blue)
        return source_data


class IdentitiesTableModel(QAbstractTableModel):

    '''
    A Qt abstract item model to display communities in a tree
    '''

    def __init__(self, community, parent=None):
        '''
        Constructor
        '''
        super().__init__(parent)
        self.community = community
        self.columns_titles = {
                               'uid': self.tr('UID'),
                               'pubkey': self.tr('Pubkey'),
                               'renewed': self.tr('Renewed'),
                               'expiration': self.tr('Expiration')}
        self.columns_ids = ('uid', 'pubkey', 'renewed', 'expiration')
        self.identities_data = []

    @property
    def pubkeys(self):
        '''
        Get pubkeys of displayed identities
        '''
        return [i[1] for i in self.identities_data]

    def identity_data(self, person):
        parameters = self.community.parameters
        try:
            join_block = person.membership(self.community)['blockNumber']
            try:
                join_date = self.community.get_block(join_block).mediantime
                expiration_date = join_date + parameters['sigValidity']
            except NoPeerAvailable:
                join_date = None
                expiration_date = None
        except MembershipNotFoundError:
            join_date = None
            expiration_date = None

        return (person.uid, person.pubkey, join_date, expiration_date)

    def refresh_identities(self, persons):
        logging.debug("Refresh {0} identities".format(len(persons)))
        self.identities_data = []
        self.beginResetModel()
        for person in persons:
            self.identities_data.append(self.identity_data(person))
        self.endResetModel()

    def rowCount(self, parent):
        return len(self.identities_data)

    def columnCount(self, parent):
        return len(self.columns_ids)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            col_id = self.columns_ids[section]
            return self.columns_titles[col_id]

    def data(self, index, role):
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return self.identities_data[row][col]

    def person_index(self, pubkey):
        try:
            row = self.pubkeys.index(pubkey)
            index_start = self.index(row, 0)
            index_end = self.index(row, len(self.columns_ids))
            return (index_start, index_end)
        except ValueError:
            return (QModelIndex(), QModelIndex())

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled
