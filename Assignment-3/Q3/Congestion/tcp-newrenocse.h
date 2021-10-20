/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright (c) 2014 Natale Patriciello, <natale.patriciello@gmail.com>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 */

#ifndef TCPNEWRENOCSE_H
#define TCPNEWRENOCSE_H

#include "ns3/tcp-congestion-ops.h"
#include "ns3/tcp-recovery-ops.h"

namespace ns3 {

/**
 * \ingroup congestionOps
 *
 * \brief An implementation of TCP HighSpeed
 *
 * TCP HighSpeed is designed for high-capacity channels or, in general, for
 * TCP connections with large congestion windows.
 * Conceptually, with respect to the standard TCP, HighSpeed makes the
 * cWnd grow faster during the probing phases and accelerates the
 * cWnd recovery from losses.
 * This behavior is executed only when the window grows beyond a
 * certain threshold, which allows TCP Highspeed to be friendly with standard
 * TCP in environments with heavy congestion, without introducing new dangers
 * of congestion collapse.
 * At the core of TCP HighSpeed there are two functions, a(w) and b(w), which respectively
 * specify the cWnd growth addendum and the cWnd reduction factor when
 * given an actual cWnd value w.
 *
 * More information: http://dl.acm.org/citation.cfm?id=2756518
 */
class TcpNewRenoCSE : public TcpCongestionOps
{
public:
  /**
   * \brief Get the type ID.
   * \return the object TypeId
   */
  static TypeId GetTypeId (void);

  TcpNewRenoCSE ();

  /**
   * \brief Copy constructor.
   * \param sock object to copy.
   */
  TcpNewRenoCSE (const TcpNewRenoCSE& sock);

  ~TcpNewRenoCSE ();

  std::string GetName () const;

  virtual void IncreaseWindow (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked);
  virtual uint32_t GetSsThresh (Ptr<const TcpSocketState> tcb,
                                uint32_t bytesInFlight);

  virtual Ptr<TcpCongestionOps> Fork ();

protected:
  virtual uint32_t SlowStart (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked);
  virtual void CongestionAvoidance (Ptr<TcpSocketState> tcb, uint32_t segmentsAcked);
};

} // namespace ns3

#endif // TCPCONGESTIONOPS_H
