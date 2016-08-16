from Lock import ThreadLock

class ThreadBaseLock(object):
    m_lock = ThreadLock.SourceLock()