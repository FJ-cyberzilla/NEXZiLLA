#!/usr/bin/env python3
import asyncio
from cyber_intel_sdk import AsyncCyberIntelSDK

async def main():
    # Using async context manager
    async with AsyncCyberIntelSDK("http://localhost:8007") as sdk:
        # Analyze a target
        threat_intel = await sdk.analyze_threat("example.com")
        print(f"Threat level: {threat_intel.threat_level.value}")
        
        # Get forecast
        forecast = await sdk.forecast_threats("example.com", "2024-12-01")
        print(f"Predicted risk: {forecast.predicted_risk:.0%}")
        
        # Generate report
        report = await sdk.generate_report({
            "threat_intel": threat_intel.to_dict(),
            "forecast": forecast.to_dict()
        })
        print(f"Report generated: {report.report_id}")

# Synchronous usage
from cyber_intel_sdk import SyncCyberIntelSDK

def sync_example():
    sdk = SyncCyberIntelSDK("http://localhost:8007")
    threat_intel = sdk.analyze_threat("example.com")
    print(f"Sync analysis: {threat_intel.threat_level.value}")

if __name__ == "__main__":
    asyncio.run(main())
    sync_example()
