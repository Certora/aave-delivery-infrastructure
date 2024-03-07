// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title ICrossChainControllerRev2
 * @author BGD Labs
 * @notice interface containing re initialization method
 */
interface ICrossChainControllerRev2 {
  /**
   * @notice method called to re initialize the proxy
   */
  function initializeRevision() external;
}
